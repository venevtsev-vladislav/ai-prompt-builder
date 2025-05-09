# core/prompt_logic.py

import requests
import streamlit as st
from constants import BACKEND_URL

def validate_prompt_input(name: str, hint: str) -> bool:
    if not name.strip():
        st.error("❌ Название промта не может быть пустым.")
        return False
    if not hint.strip():
        st.error("❌ Подсказка промта не может быть пустой.")
        return False
    return True

def save_prompt(name: str, hint: str, param1: str, param2: str):
    # Обновляем локальное состояние
    st.session_state.prompts[name] = {
        "instruction": hint,
        "param1": param1,
        "param2": param2
    }

    user_id = st.session_state.get("user", {}).get("id", "")
    if not user_id:
        st.error("❌ Нет user_id")
        return

    payload = {
        "name": name,
        "instruction": hint,
        "param1": param1,
        "param2": param2,
        "user_id": user_id
    }

    headers = {}
    if "access_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['access_token']}"

    try:
        # 🔁 Попытка обновления
        put_url = f"{BACKEND_URL}/prompts/{user_id}/{name}"
        put_response = requests.put(put_url, json=payload, headers=headers)

        if put_response.status_code == 200:
            st.success("✅ Промт обновлён!")
            return

        # 📤 Если не найден → создаём
        post_url = "http://localhost:8000/prompts"
        post_response = requests.post(post_url, json=payload, headers=headers)
        print("📡 Ответ от сервера:", post_response.status_code, post_response.text)

        if post_response.status_code == 200:
            st.success("✅ Промт создан!")
        else:
            st.warning("⚠️ Не удалось сохранить промт.")
    except Exception as e:
        st.error(f"❌ Ошибка при сохранении: {e}")

def delete_prompt(name: str):
    user_id = st.session_state.get("user", {}).get("id", "")
    if not user_id:
        st.warning("⚠️ Нет user_id")

    url = f"{BACKEND_URL}/prompts/{user_id}/{name}"
    try:
        response = requests.delete(url)
        print(f"🧨 DELETE URL: {url}")
        if response.status_code == 200:
            st.success("🗑️ Промт удалён!")
            st.session_state.prompts.pop(name, None)
            if st.session_state.selected_prompt == name:
                st.session_state.selected_prompt = None
            st.rerun()
        else:
            st.error("❌ Не удалось удалить промт.")
    except Exception as e:
        st.error(f"❌ Ошибка удаления: {e}")