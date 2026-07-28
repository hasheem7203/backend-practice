from fastapi import FastAPI
from auth import supabase 

app = FastAPI(title="Auth API")

@app.on_event("startup")
def startup_message():
    print("Server running and connected to Supabase")
    