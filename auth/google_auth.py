import streamlit as st
from streamlit_google_auth import Authenticate
import json
from services.supabase_service import sync_user_to_supabase  # 🔗 Синхронизация с Supabase

# 📌 Выводим client_id для отладки (удобно при переключении проектов Google)
with open("google_credentials.json") as f:
    creds = json.load(f)
    print("🧪 Используемый client_id:", creds["web"]["client_id"])


def get_authenticator():
    """Создаёт или возвращает кэшированный объект авторизатора Google"""
    if "authenticator" not in st.session_state:
        st.session_state["authenticator"] = Authenticate(
            secret_credentials_path="google_credentials.json",
            cookie_name="my_cookie",
            cookie_key="super_secret_key",
            redirect_uri="http://localhost:8501"
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