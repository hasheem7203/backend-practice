import os 
from dotenv import load_dotenv
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from supabase import create_client,client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPBASE_URL,SUPABASE_KEY must be set in .env")

supabase: client= create_client(SUPABASE_URL,SUPABASE_KEY)