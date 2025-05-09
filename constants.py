# constants.py Опции UI, фиксированные значения

import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

LENGTH_OPTIONS = ["Коротко", "Средне", "Развернуто"]
TONE_OPTIONS = ["Формальный", "Неформальный", "Экспертный"]
PROMPT_PARAMS = ["-", "Длина", "Тон"]