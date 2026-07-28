from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from auth import supabase 

app = FastAPI(title="Auth API")

@app.on_event("startup")
def startup_message():
    print("Server running and connected to Supabase")
    
    
class Credentials (BaseModel):
    email: str
    password: str
    
@app.post("/auth/signup", status_code=201)
def signup(body: Credentials):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="email and password are required ")
    
    try :
        result = supabase.auth.sign_up({"email": body.email,"password": body.password})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"user": result.user}

@app.post("/auth/login",status_code=200)
def login(body:Credentials):
    if not body.email or not body.password:
        raise HTTPException(status_code=400,detail="emailand password are required")
    
    try:
        result = supabase.auth.sign_in_with_password({"email": body.email,"password": body.password})
    
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalidlogin credentials")
    
    if not result.session:
        raise HTTPException(status_code=401,detail="invalid login credentials")
    
    return{
        "access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token,
    }