# services/prompt_api.py
import requests
import streamlit as st

def send_prompt_to_api(name, instruction, param1, param2):
    payload = {
        "name": name,
        "instruction": instruction,
        "param1": param1,
        "param2": param2,
        "user_id": st.session_state.user["id"] if st.session_state.get("user") else ""
    }
    headers = {}
    if "access_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['access_token']}"
    requests.post("http://localhost:8000/prompts", json=payload, headers=headers)