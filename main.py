import logging,asyncio

from dotenv import load_dotenv
from os import getenv
from pathlib import Path

from aiogram import Bot,Dispatcher,F,types
from aiogram.filters import CommandStart,Command,or_f
from aiogram.types import FSInputFile
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError

from mykeyboard import sing_in_reply_btn,copy_text_btn,create_ad_btn,link_btn

from data import user_check,search_user_info,add_user,init_db,get_user,get_all_users_id

from utils import action_log,error_log,ERROR_PROMPT_MESSAGE,REGISTRATION_PROMPT_MESSAGE

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(levelname)s - %(filename)s: %(lineno)d - %(asctime)s - %(message)s",
    level=logging.DEBUG,
    encoding="utf-8"
)

h = logging.StreamHandler()
h.setLevel(logging.INFO) 
logging.getLogger().addHandler(h)
try:
    load_dotenv()
    bot = Bot(token = getenv("BOT_TOKEN"))
    ADMIN_ID = int(getenv("ADMIN_ID"))
except Exception as e:
    logging.critical(f"Не удалось загрузить .env файл\nОшибка: {e}")
    exit()

dp = Dispatcher()
BASE_DIR = Path(__file__).resolve().parent

class CreateAdState(StatesGroup):
    text : str = State()
    link : str = State()

@dp.message(or_f(CommandStart(),F.text == "start"))
async def start_handler(message : types.Message):
    logging.info(action_log(message))
    result = await user_check(message.from_user.id)
    if result == True:
        await message.answer("😊Добро пожаловать рады вас видеть снова!")
    elif result == False:
        await message.reply("✨Привет!\n\n➡️Чтобы продолжить отправьте ваш контакт.",reply_markup=sing_in_reply_btn())
    else:
        logging.error("Произошла ошибка в start_handler при использовании user_check")
        await message.answer(ERROR_PROMPT_MESSAGE)

@dp.message(or_f(Command("help"),F.text == "help"))
async def help_handler(message : types.Message):
    logging.info(action_log(message))
    await message.reply("📖 Помощь\n\n👤 Получение информации о контакте:\n• Откройте профиль пользователя.\n• Нажмите ⋮ (три точки).\n• Выберите «Поделиться контактом».\n• Отправьте контакт боту.\n\n🔄 Перезапуск бота:\n• Отправьте команду /start.\n\n📢 Поделиться ботом:\n• Откройте профиль бота.\n• Нажмите «Поделиться».\n• Выберите получателя и отправьте ссылку.\n\n⚠️ Бот обрабатывает только контакты, отправленные через функцию «Поделиться контактом»."
)
    
@dp.message(F.contact)
async def contact_handler(message : types.Message):
    logging.info(action_log(message))
    result = await user_check(message.from_user.id)
    if result == True:
        contact = message.contact
        cheking_id = message.contact.user_id
        if message.from_user.id == cheking_id:
            answer = await get_user(id=message.from_user.id,by_short_id=False)
            if isinstance(answer,tuple):
                logging.error(error_log([answer[1]]))
                await message.answer(ERROR_PROMPT_MESSAGE)
            else:
                await message.answer(f"✨Это Вы\n{answer}",reply_markup=copy_text_btn(answer))
                return
        else:
            new_user_checking = await user_check(cheking_id)
            if new_user_checking == False:
                user = search_user_info(contact , return_as_list = True)
                answer = search_user_info(contact)
                new_user_add = await add_user(user)
                if not new_user_add:
                    logging.error(f"Ошибка при добавлении пользователя в user-data.db user:\n{user}")
                    await message.answer(ERROR_PROMPT_MESSAGE)
                    return
                await message.answer(answer,reply_markup=copy_text_btn(answer))
            elif new_user_checking == True:
                answer = await get_user(cheking_id,by_short_id=False)
                if isinstance(answer,tuple):
                    logging.error(error_log(answer[1]))
                    await message.answer(ERROR_PROMPT_MESSAGE)
                    return
                else:
                    await message.answer(answer,reply_markup=copy_text_btn(answer))
            else:
                logging.error(f"Произошла ошибка при поиске информации в user_data.db при использовании contact_handler при user_check({cheking_id})")
                await message.answer(ERROR_PROMPT_MESSAGE)
    elif result == False:
        contact = message.contact
        if message.from_user.id == contact.user_id:
            user = search_user_info(contact=contact , message=message , return_as_list = True , is_user_contact=True)
            new_user_add = await add_user(user)
            if not new_user_add:
                logging.error(f"Ошибка при добавлении пользователя в user-data.db user:\n{user}")
                await message.answer(ERROR_PROMPT_MESSAGE)
                return
            await message.answer("Добро пожаловать вы прошли регистрацию")
        else:
            await message.answer(REGISTRATION_PROMPT_MESSAGE,reply_markup=sing_in_reply_btn())
    else:
        logging.error(f"Произошла ошибка в contact_handler при использовании user_check: {result}")
        await message.answer(f"{ERROR_PROMPT_MESSAGE}\nРеконмендация: Попытайтесь отправить другой контакт.")

@dp.message(or_f(Command('checkuser'),F.text == 'checkuser'))
async def check_user_handler(message : types.Message):
    logging.info(action_log(message))
    result = await user_check(message.from_user.id)
    if result == True:
        await message.answer("📎 Отправьте контакт через скрепку\nЛибо зайдите в профиль контакта затем нажмите на троеточие и нажмите 'Поделится контактом'.")
    elif result == False:
        await message.answer(REGISTRATION_PROMPT_MESSAGE,reply_markup=sing_in_reply_btn())
    else:
        await message.answer(ERROR_PROMPT_MESSAGE)
@dp.message(or_f(Command('share'),F.text == 'share'))
async def share_handler(message : types.Message):
    logging.info(action_log(message))
    await message.answer_photo(FSInputFile(BASE_DIR / 'photo'/ 'qr-code.png'),caption="➡️Поделитесь QR кодом\nИли отправьте:\nhttps://t.me/backendlearning0_bot\n@backendlearning0_bot")

@dp.message(or_f(Command('admin'),F.text == 'admin'))
async def admin_handler(message : types.Message):
    logging.info(action_log(message))
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Рады вас видеть {message.from_user.full_name.title() or 'Админ'}!",reply_markup=create_ad_btn())
    else:
        await message.answer("➡️❕У вас нет доступа к этой команде.")

@dp.callback_query(F.data == "create_ad")
async def create_ad_handler(callback : types.CallbackQuery , state : FSMContext):
    await state.set_state(CreateAdState.text)
    await callback.message.edit_text("➡️Отправьте текст вашей рекламы")
    await callback.answer()

@dp.message(CreateAdState.text)
async def get_ad_text_handler(message : types.Message , state : FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(CreateAdState.link)
    await message.answer("Отлично! Отправьте ссылку на сайт / соц. сети рекламодателя")

@dp.message(CreateAdState.link)
async def get_ad_link_handler(message : types.Message , state : FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()

    text = data['text']
    link = data['link']

    users = await get_all_users_id()

    if users is False:
        logging.error("При использовании функции get_all_users_id в get_ad_link_handler произошла ошибка!")
        await message.answer(ERROR_PROMPT_MESSAGE)
        state.clear()
        return
    else:
        for (user_id,) in users:
            if user_id is None:
                continue
            try:
                await asyncio.sleep(0.05)
                await bot.send_message(chat_id=user_id,text=text,reply_markup=link_btn(link=link))
            except TelegramForbiddenError as e:
                logging.error(f"{error_log(e)}\nПользователь {user_id} заблокировал бота или не запускал его")
        await message.answer("✅Реклама отправленна!")
        await state.clear()


async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.info("\n\nПрограмма запущенна...")
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Не удалось запустить программу,ошибка: {e}")