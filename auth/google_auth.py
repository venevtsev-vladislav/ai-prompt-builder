import streamlit as st
from streamlit_google_auth import Authenticate
import json
from services.supabase_service import sync_user_to_supabase  # 🔗 Синхронизация с Supabase
from constants import FRONTEND_URL
import os

# Собираем словарь как будто он из google_credentials.json
creds = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": "coastal-range-459218-g1",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": os.getenv("GOOGLE_REDIRECT_URIS", "").split(","),
        "javascript_origins": os.getenv("GOOGLE_ORIGINS", "").split(",")
    }
}

print("🧪 Используемый client_id:", creds["web"]["client_id"])

# Сохраняем временно на диск, т.к. библиотека ожидает путь
temp_cred_path = "/tmp/google_credentials.json"
with open(temp_cred_path, "w") as f:
    json.dump(creds, f)

def get_authenticator():
    """Создаёт или возвращает кэшированный объект авторизатора Google"""
    if "authenticator" not in st.session_state:
        st.session_state["authenticator"] = Authenticate(
            secret_credentials_path=temp_cred_path,
            cookie_name="my_cookie",
            cookie_key="super_secret_key",
            redirect_uri = FRONTEND_URL
        )
    return st.session_state["authenticator"]


def setup_authentication():
    """Основная логика авторизации и привязки пользователя к Supabase"""
    # 🧩 Обязательно инициализируем ключ, иначе `check_authentification()` может упасть
    if "connected" not in st.session_state:
        st.session_state["connected"] = False

    authenticator = get_authenticator()
    authenticator.check_authentification()
    authenticator.login()

    if st.session_state.get("connected"):
        # ✅ Получаем user_info от Google
        user_info = st.session_state.get("user_info", {})

        # 🔗 Сохраняем/обновляем пользователя в Supabase и получаем UUID
        user_uuid = sync_user_to_supabase(user_info)

        # 💾 Сохраняем в session_state
        st.session_state["user"] = {
            "id": user_uuid,  # ☑️ Это UUID из таблицы `users`, используется как FK в prompts
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "avatar_url": user_info.get("picture"),
        }
        return user_info

    return None