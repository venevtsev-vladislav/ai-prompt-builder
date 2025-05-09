# services/supabase_service.py

from supabase import create_client, Client
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # 🔹 Загружаем переменные окружения из .env до их использования

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_user_to_supabase(user_info: dict) -> str:
    """
    Создаёт или обновляет пользователя по email и возвращает его UUID.
    Если пользователь уже существует, читаем его ID.
    """
    email = user_info["email"]

    # 🔍 Проверяем, есть ли уже этот пользователь
    existing = supabase.table("users").select("id").eq("email", email).execute()
    if existing.data:
        return existing.data[0]["id"]  # Если есть — возвращаем UUID

    # 📅 Если нет — добавляем нового
    result = supabase.table("users").insert({
        "email": email,
        "name": user_info.get("name"),
        "avatar_url": user_info.get("picture", ""),
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    return result.data[0]["id"]  # UUID только что созданного пользователя

def fetch_prompts(user_id: str):
    """ Чтение всех промтов для конкретного user_id """
    return supabase.table("prompts").select("*").eq("user_id", user_id).execute()

def save_prompt_to_supabase(prompt: dict):
    """ Обновляет или добавляет промт в базу """
    return supabase.table("prompts").upsert(prompt).execute()
