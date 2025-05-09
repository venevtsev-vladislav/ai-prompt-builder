# build_prompt, возможно шаблоны
def build_prompt(task: str, tone: str, length: str, user_input: str):
    base = f"Ты — AI, помоги с задачей: {task}. Ответ должен быть в {tone} стиле, длиной: {length}.\n\n"
    return base + f"Текст: {user_input}"
