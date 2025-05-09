# app.py Точка входа, сборка интерфейса

import streamlit as st
import logging
from auth.google_auth import setup_authentication
#from services.supabase_service import sync_user_to_supabase
from ui.layout import render_main_ui
from state import init_state
from services.supabase_service import fetch_prompts

init_state()


st.set_page_config(page_title="AI Prompt Builder", layout="centered")
logging.basicConfig(level=logging.INFO)
logging.info("🚀 Запуск приложения AI Prompt Builder")

# Авторизация
setup_authentication()

# Загружаем промты в session_state
if st.session_state.get("user"):
    user_id = st.session_state.user["id"]
    prompts_response = fetch_prompts(user_id)
    prompts_data = prompts_response.data
    st.session_state.prompts = {
        item["name"]: {
            "instruction": item["instruction"],
            "param1": item["param1"],
            "param2": item["param2"]
        }
        for item in prompts_data
    }

# Отрисовка UI
render_main_ui()

if st.button("📋 Скопировать токен"):
    access_token = st.session_state.get("user", {}).get("access_token")
    if access_token:
        st.success("🔑 Токен получен:")
        st.code(f"Bearer {access_token}", language="text")
    else:
        st.error("❌ Токен не найден. Убедитесь, что вы вошли в систему.")