from aiogram import types

REGISTRATION_PROMPT_MESSAGE = "❕Пожалуйста чтобы пользоватся нашими услугами и поиском данных пройдите регистрацию"

ERROR_PROMPT_MESSAGE = "❕Приносим свои извенения\nПроизошла ошибка попробуйте чуть снова позже."


def action_log(message : types.Message , content_name : str = '[no text]'):
    return f"@{message.from_user.username or message.from_user.full_name} отправил {message.text or message.contact or content_name}"
def error_log(error : str):
    return f"Не удалось выполнить операцию ошибка {error}"