# ui/sidebar.py
import streamlit as st
import json
from auth.google_auth import get_authenticator
from core.prompt_logic import delete_prompt

def render_sidebar():
    st.sidebar.markdown("#### ✨ AI Prompt Builder")

    render_prompt_section()
    render_chat_list()
    render_export_button()
    render_user_info()  # 👈 Добавили этот вызов

def render_prompt_section():
    col_title, col_plus = st.sidebar.columns([0.9, 0.1])
    with col_title:
        st.markdown("#### 🧠 Промты")
    with col_plus:
        if st.button("➕", key="add_prompt_btn"):
            st.session_state.edit_mode = True
            st.session_state.adding_new = True

    prompt_usage = {}
    for i in reversed(range(len(st.session_state.get("history", [])))):
        item = st.session_state.history[i]
        if isinstance(item, dict) and "prompt_name" in item:
            prompt_usage[item["prompt_name"]] = i

    prompts = list(st.session_state.prompts) if isinstance(st.session_state.prompts, dict) else []
    sorted_prompts = sorted(prompts, key=lambda x: -prompt_usage.get(x, -1))

    for name in sorted_prompts:
        cols = st.sidebar.columns([0.7, 0.15, 0.15])
        is_selected = name == st.session_state.get("selected_prompt")
        btn_style = "font-weight: bold; background-color: #d8f3ff;" if is_selected else ""

        if cols[0].button(name, key=f"select_{name}"):
            st.session_state.selected_prompt = name
            st.session_state.edit_mode = False
            st.session_state.adding_new = False
            st.rerun()

        if cols[1].button("✏️", key=f"edit_{name}"):
            st.session_state.selected_prompt = name
            st.session_state.edit_mode = True
            st.session_state.adding_new = False

        if cols[2].button("🗑️", key=f"delete_{name}"):
            delete_prompt(name)
            st.session_state.prompts.pop(name, None)
            if st.session_state.selected_prompt == name:
                st.session_state.selected_prompt = next(iter(st.session_state.prompts), None)
            st.rerun()

def render_chat_list():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Чаты")

    sorted_chats = sorted(
        [chat for chat in st.session_state.get("history", []) if isinstance(chat, dict) and "last_used" in chat],
        key=lambda x: x["last_used"],
        reverse=True
    )[:10]

    container_style = "max-height: 300px; overflow-y: auto;"
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
    for chat in sorted_chats:
        chat_name = chat.get("prompt_name", "Без названия")
        chat_id = chat.get("id")
        last_msg = chat.get("messages", [{}])[-1].get("content", "")
        preview = last_msg[:40].replace("\n", " ") + ("..." if len(last_msg) > 40 else "")
        label = f"{chat_name}: {preview}"
        if st.button(label, key=f"chat_{chat_id}"):
            st.session_state.selected_chat_id = chat_id
            st.session_state.selected_prompt = chat_name
            st.session_state.chat_history = chat.get("messages", [])
            st.session_state.edit_mode = False
            st.session_state.adding_new = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_export_button():
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 📤 Экспорт промтов")
    st.sidebar.download_button(
        label="📥 Скачать",
        data=json.dumps(st.session_state.prompts, indent=2, ensure_ascii=False),
        file_name="prompts_export.json",
        mime="application/json"
    )

def render_user_info():
    user = st.session_state.get("user")

    if user:
        col1, col2 = st.sidebar.columns([0.2, 0.8])
        with col1:
            if user.get("avatar_url"):
                st.image(user["avatar_url"], width=32)
        with col2:
            st.markdown(f"**{user.get('name', 'Пользователь')}**")

        if st.sidebar.button("🚪 Выйти", key="logout_btn"):
            from auth.google_auth import get_authenticator
            authenticator = get_authenticator()
            authenticator.logout()
            for key in ["user", "user_info", "access_token", "connected"]:
                st.session_state.pop(key, None)
            st.rerun()