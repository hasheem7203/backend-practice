import os 
import json
import re
import time
import random

from dotenv import load_dotenv
from fastapi import FastAPI , HTTPException
from schema import TriageInput,TriageOutput,Category,Urgency,Team
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from openai import OpenAI , APITimeoutError , RateLimitError , APIStatusError
from datetime import datetime,timezone
from pydantic import ValidationError

load_dotenv()

app = FastAPI()

def load_prompt(version : str ="v1")-> str:
    path = f"prompts/triage-{version}.md"
    with open(path,"r",encoding = "utf-8") as f:
        return f.read()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: '{field}' — {first_error['msg']}"},
    )

def extract_json(raw_text:str ) -> dict:
    """strip code fefnces / extra text and parse the model.s reply as JSON."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$","", cleaned.strip())
    return json.loads(cleaned)

def call_model(client,model,system_prompt,user_text,repair_note:str = None):
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_text},
    ]
    if repair_note:
        messages.append({"role":"user","content":repair_note})
        
    res = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=messages,
    )
    
    return res.choices[0].message.content


def call_model_with_retry(client,model,system_prompt,user_text ,repair_note=None,max_retries=2):
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return call_model(client,model,system_prompt,user_text,repair_note=repair_note)
        except APITimeoutError as e:
            last_exception = e 
        except RateLimitError as e:
            last_exception = e
        except APIStatusError as e:
            if e.status_code in (401,403):
                raise
            if e.status_code // 100 == 5:
                last_exception = e
            else :
                raise
        
        if attempt < max_retries:
            wait = (2** attempt) + random.uniform(0,0.5)
            time.sleep(wait)

    raise last_exception

@app.post("/triage",response_model=TriageOutput)
def triage(payload: TriageInput):
    if os.environ.get("LLM_STUB") == "1":
        return TriageOutput(
            category=Category.other,
            urgency= Urgency.low,
            suggested_team = Team.general_support,
            confidence = 0.42,
            reason = "Stub mode: no model was called.",
        )
        
    system_prompt = load_prompt("v1")
    
    client = OpenAI(
        base_url=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        timeout=30.0,
    )
    
    model=os.environ["LLM_MODEL"]
    
    try:
        raw_text = call_model_with_retry(client,model,system_prompt,payload.text)
    except APITimeoutError:
        raise HTTPException(status_code=504,detail="Model call timeout.")
    except RateLimitError:
        raise HTTPException(status_code=429,detail="rate limited after retries")
    
    error_detail = None
    try:
        data = extract_json(raw_text)
        result = TriageOutput(**data)
        return result
    except (json.JSONDecodeError,ValidationError) as e:
        error_detail = str(e)
        
    repair_note = (
        f"your previous answer was rejected for this reason: {error_detail}."
        f"your previous answer was : {raw_text}. "
        "return only corrected json matching the schema."
    )
    
    try:
        raw_text_2 = call_model_with_retry(client,model,system_prompt,payload.text,repair_note=repair_note)
    except APITimeoutError:
        raise HTTPException(status_code=504,detail="Model call timed out")
    except RateLimitError :
        raise HTTPException(status_code=429,detail="rate limited after reties. ")
    
    try:
        data= extract_json(raw_text_2)
        result = TriageOutput(**data)
        return result
    except (json.JSONDecodeError,ValidationError) as e:
        error_detail_2 = str(e)
        
    os.makedirs("logs", exist_ok=True)
    with open("logs/quarantine.jsonl","a",encoding = "utf-8") as f:
        f.write(json.dumps({
            "timestampt": datetime.now(timezone.utc).isoformat(),
            "input": payload.text,
            "prompt_version" : "v1",
            "attemp_1_raw": raw_text,
            "attemp_1_error":error_detail,
            "attemp_2_raw": raw_text_2,
            "attemp_2_error":error_detail_2,
        }) + "\n")
    
    raise HTTPException(status_code=422,detail="model could not produce a valid response after repair attempt.")