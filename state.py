# state.py Инициализация и управление session_state
import streamlit as st

def init_state():
    defaults = {
        "prompts": {},
        "selected_prompt": "Упростить",
        "edit_mode": False,
        "adding_new": False,
        "history": [],
        "selected_chat_id": None,
        "chat_history": [],
        "param1": "Коротко",
        "param2": "Формальный",
        "user": None,
        "show_settings": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value