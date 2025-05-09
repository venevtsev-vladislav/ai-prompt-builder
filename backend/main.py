#backend/main.py
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from supabase import create_client
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

app = FastAPI()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажи домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return JSONResponse(
        content={"status": "Backend работает"},
        media_type="application/json; charset=utf-8"
    )

class Prompt(BaseModel):
    name: str
    instruction: str
    param1: str = ""
    param2: str = ""
    user_id: str

@app.get("/prompts", response_model=List[Prompt])
def get_prompts():
    data = supabase.table("prompts").select("*").order("updated_at", desc=True).execute()
    return data.data

@app.post("/prompts", response_model=Prompt)
def add_prompt(prompt: Prompt):
    print("📥 POST /prompts получен:", prompt.dict())
    data = supabase.table("prompts").insert({
        "name": prompt.name,
        "instruction": prompt.instruction,
        "param1": prompt.param1,
        "param2": prompt.param2,
        "user_id": prompt.user_id
    }).execute()
    print("📤 Supabase insert response:", data)
    return data.data[0]

@app.put("/prompts/{user_id}/{name}", response_model=Prompt)
def update_prompt(user_id: str, name: str, prompt: Prompt):
    """Обновляет промт по user_id + name"""
    print("📥 PUT /prompts получен:", prompt.dict())
    response = supabase.table("prompts").update({
        "instruction": prompt.instruction,
        "param1": prompt.param1,
        "param2": prompt.param2
    }).eq("user_id", user_id).eq("name", name).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Prompt not found")
    print("📤 Supabase insert response:", data)
    return response.data[0]


@app.delete("/prompts/{user_id}/{name}")
def delete_prompt(user_id: str, name: str):
    """Удаляет промт"""
    response = supabase.table("prompts").delete().eq("user_id", user_id).eq("name", name).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Prompt not found")
    print(f"🗑️ DELETE /prompts for user_id={user_id}, name={name}")
    print(f"🗑️ DELETE response: {response}")
    return {"status": "deleted"}