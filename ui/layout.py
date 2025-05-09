# ui/layout.py — визуальные компоненты (чат, редактор промтов и т.п.)

import streamlit as st
from ui.sidebar import render_sidebar
from constants import LENGTH_OPTIONS, TONE_OPTIONS
from core.prompt_logic import save_prompt, validate_prompt_input

def render_main_ui():
    # 🛑 Не авторизован → показать только кнопку входа
    if not st.session_state.get("user"):
        st.markdown("""
                <div style='display: flex; justify-content: center; align-items: center; height: 80vh;'>
                    <a href="?">
                        <button style="font-size:16px; padding: 10px 20px;'>🔐 Войти через Google</button>
                    </a>
                </div>
            """, unsafe_allow_html=True)
        return  # ❗️этот return имеет тот же отступ, что и if

    # ✅ Авторизован → отрисовываем основное UI
    from ui.sidebar import render_sidebar  # можно оставить, если хочется избегать цикличности
    render_sidebar()

    if st.session_state.get("edit_mode", False):
        name = "" if st.session_state.get("adding_new") else st.session_state.get("selected_prompt")
        data = st.session_state.prompts.get(name, None)
        render_prompt_editor(name, data)
    elif st.session_state.get("selected_prompt"):
        from ui.layout import display_messages, render_chat_ui
        display_messages()
        submitted, user_msg = render_chat_ui()
        if submitted:
            from services.gpt_service import generate_response
            response = generate_response(user_msg)
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

def render_chat_ui():
    """Интерфейс общения (чат)"""
    st.markdown("""<style>.block-container {padding-bottom: 120px;}</style>""", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=False):
        user_msg = st.text_area(f"📌 {st.session_state.selected_prompt}\nВведите сообщение:", key="chat_input", height=150)
        cols = st.columns([1, 1, 1, 1, 1])

        submitted = cols[0].form_submit_button("Отправить")
        if cols[1].form_submit_button("⚙️", use_container_width=True):
            st.session_state.show_settings = not st.session_state.get("show_settings", False)
        if cols[2].form_submit_button("💬", use_container_width=True):
            pass  # future
        if cols[3].form_submit_button("💾", use_container_width=True):
            save_current_chat()
        if cols[4].form_submit_button("🧹", use_container_width=True):
            st.session_state.chat_history.clear()

        if st.session_state.get("show_settings", False):
            st.markdown("### ⚙️ Настройки")
            st.session_state.param1 = st.selectbox("Длина", LENGTH_OPTIONS, index=LENGTH_OPTIONS.index(st.session_state.param1))
            st.session_state.param2 = st.selectbox("Тон", TONE_OPTIONS, index=TONE_OPTIONS.index(st.session_state.param2))

        return submitted, user_msg

def render_prompt_editor(name=None, data=None):
    """UI редактора промта"""
    is_new = name is None
    default_data = {
        "instruction": "",
        "param1": "Длина",
        "param2": "Тон"
    }
    data = data or default_data

    new_name = st.text_input("Название промта", value=name or "")
    hint = st.text_area("Подсказка", value=data.get("instruction", ""), height=100)
    param1 = st.selectbox("Параметр 1", ["-", "Длина", "Тон"], index=1)
    param2 = st.selectbox("Параметр 2", ["-", "Длина", "Тон"], index=2)

    if st.button("Сохранить"):
        if validate_prompt_input(new_name, hint):
            save_prompt(new_name, hint, param1, param2)
            st.session_state.selected_prompt = new_name
            st.session_state.edit_mode = False
            st.session_state.adding_new = False
            st.rerun()

def display_messages():
    """Показ истории сообщений"""
    for msg in st.session_state.chat_history:
        is_user = msg["role"] == "user"
        align = "flex-end" if is_user else "flex-start"
        bg = "#e6f7ff" if is_user else "#f5f5f5"
        icon = "🧑‍💻" if is_user else "🤖"
        st.markdown(f"""
            <div style='display: flex; justify-content: {align}; margin: 5px 0;'>
                <div style='background-color: {bg}; padding: 10px; border-radius: 10px; max-width: 80%;'>
                    <div style='font-size: 0.9em;'>{icon} {msg['content']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def save_current_chat():
    """Сохраняет последнее сообщение в историю"""
    if st.session_state.chat_history:
        last = st.session_state.chat_history[-1]
        st.session_state.history.append({
            "prompt_name": st.session_state.selected_prompt,
            "input": last["content"]
        })