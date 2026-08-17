import os 
from dotenv import load_dotenv
from fastapi import FastAPI , HTTPException
from schema import TriageInput,TriageOutput,Category,Urgency,Team
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: '{field}' — {first_error['msg']}"},
    )

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
        
    raise HTTPException(status_code=500,detail="Real model call not implemented yet (Stage 2)")