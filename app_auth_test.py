# app_auth_test.py

import streamlit as st
from streamlit_google_auth import Authenticate

st.set_page_config(page_title="Google Auth Test", layout="centered")
st.title("🔐 Google Авторизация через streamlit-google-auth")

# Инициализируем аутентификатор
authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',  # Убедись, что файл существует и содержит client_id + secret
    cookie_name='my_app_auth_cookie',
    cookie_key='super_secure_key_here',
    redirect_uri='http://localhost:8501',
    cookie_expiry_days=1
)

# Проверка аутентификации
authenticator.check_authentification()

# Кнопка логина
authenticator.login()

if st.session_state.get('connected'):
    user_info = st.session_state.get('user_info', {})
    st.success("✅ Вы успешно вошли в систему")
    st.image(user_info.get('picture', ''), width=100)
    st.write(f"👤 Имя: {user_info.get('name', 'Неизвестно')}")
    st.write(f"📧 Email: {user_info.get('email', 'Неизвестен')}")

    if st.button("🚪 Выйти"):
        authenticator.logout()
else:
    st.warning("⛔ Вы не авторизованы. Пожалуйста, войдите через Google.")
