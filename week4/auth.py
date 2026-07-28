import os 
from dotenv import load_dotenv
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from supabase import create_client,client
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPBASE_URL,SUPABASE_KEY must be set in .env")

supabase: client= create_client(SUPABASE_URL,SUPABASE_KEY)


bearer_scheme= HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail= "Access token Required")

    token =credentials.credentials
    try:
        response =supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401,detail="invalid or expired token")
    
    if response is None or response.user is None:
        raise HTTPException(status_code=401,detail="Invalid or expired Token")
    
    return response.user