from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram.types import CopyTextButton

def sing_in_reply_btn():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Продолжить",request_contact=True)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите на кнопку чтобы добавить контакт."
)

def copy_text_btn(text : str):
    builder = InlineKeyboardBuilder()

    builder.button(text="Скопировать" , copy_text=CopyTextButton(text=text))

    return builder.as_markup()

def link_btn(link : str):
    builder = InlineKeyboardBuilder()

    builder.button(text="Перейти" , url=link)

    return builder.as_markup()

def create_ad_btn():
    builder = InlineKeyboardBuilder()

    builder.button(text="Добавить рекламу",callback_data="create_ad")

    return builder.as_markup()