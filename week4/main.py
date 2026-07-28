from fastapi import FastAPI , HTTPException, Header
from pydantic import BaseModel
from typing import Optional 
from auth import supabase


app = FastAPI(title="Auth API")

@app.on_event("startup")
def startup_message():
    print("Server running and connected to Supabase")
    
    
class Credentials (BaseModel):
    email: str
    password: str
    
@app.get("/public/info",status_code=200)
def public_info():
    return {"message":"welcome! This info is public."}


@app.get("/protected/profile",status_code=200)
def profile(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer ") or len(authorization.split(" ")) < 2:
        raise HTTPException(status_code=401, detail= "Access token Required")

    token = authorization.split(" ")[1]    
    try:
        response =supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401,detail="invalid or expired token")
    
    if response is None or response.user is None:
        raise HTTPException(status_code=401,detail="Invalid or expired Token")
    
    user = response.user
    return {
        "id":user.id,
        "email":user.email,
        "created_at": user.created_at,
    }


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
    
    
 #   Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6ImFjNjY2OGNkLTFkNGEtNDFmNi1hOGZlLWY2ZGI0OTVhMjBiNyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2pid210dHVmZGJlYmZrb21weHd1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3YWNjMzVjMC1iYWFhLTRmZTktYmMyYS1jMDE0MDVjZjRiZDMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg1MjU5ODQ2LCJpYXQiOjE3ODUyNTYyNDYsImVtYWlsIjoibXVoYW1tYWRoYXNoZWVtc2h1amFAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im11aGFtbWFkaGFzaGVlbXNodWphQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjdhY2MzNWMwLWJhYWEtNGZlOS1iYzJhLWMwMTQwNWNmNGJkMyJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzg1MjU2MjQ2fV0sInNlc3Npb25faWQiOiJiZGZjMTRiMi1iOGEyLTQzMjYtODg3Ny1lZmFhZTRiZWVkZDQiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.4zFT8QIWm_Excdpx3wfLq-nn1pvT4zb0bD0XRfzWesJEfF0g4hJjRb3dgV5PLM52kzQT5aPkrPzT7uIYhLRuxQ
 
 
#  $headers = @{ "Authorization" = "Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6ImFjNjY2OGNkLTFkNGEtNDFmNi1hOGZlLWY2ZGI0OTVhMjBiNyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2pid210dHVmZGJlYmZrb21weHd1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3YWNjMzVjMC1iYWFhLTRmZTktYmMyYS1jMDE0MDVjZjRiZDMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg1MjU5ODQ2LCJpYXQiOjE3ODUyNTYyNDYsImVtYWlsIjoibXVoYW1tYWRoYXNoZWVtc2h1amFAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Im11aGFtbWFkaGFzaGVlbXNodWphQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjdhY2MzNWMwLWJhYWEtNGZlOS1iYzJhLWMwMTQwNWNmNGJkMyJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzg1MjU2MjQ2fV0sInNlc3Npb25faWQiOiJiZGZjMTRiMi1iOGEyLTQzMjYtODg3Ny1lZmFhZTRiZWVkZDQiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.4zFT8QIWm_Excdpx3wfLq-nn1pvT4zb0bD0XRfzWesJEfF0g4hJjRb3dgV5PLM52kzQT5aPkrPzT7uIYhLRuxQ" }
# Invoke-RestMethod -Uri "http://localhost:8000/protected/profile" -Method GET -Headers $headers