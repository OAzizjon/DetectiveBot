import aiosqlite
from aiogram import types

from phonenumbers import parse,is_valid_number,NumberParseException
from phonenumbers import geocoder,carrier
from phonenumbers import PhoneNumberFormat,format_number
from utils import error_log

async def init_db():
    async with aiosqlite.connect("user_data.db") as conn:

        await conn.execute("""CREATE TABLE IF NOT EXISTS users(
            short_id INTEGER PRIMARY KEY,
            user_own_id INTEGER UNIQUE,
            full_name TEXT,
            username TEXT UNIQUE,
            phone_number TEXT,
            country TEXT,
            operator TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        
        await conn.commit()

        
async def user_check(user_id):
    async with aiosqlite.connect("user_data.db") as conn:
        try:
            cur = await conn.cursor()
            await cur.execute("SELECT 1 FROM users WHERE user_own_id = ? LIMIT 1",(user_id,))

            result = await cur.fetchone()
            if result:
                return True
            else:
                return False
        except aiosqlite.Error as e:
            return None

async def get_user(id : int , by_short_id : bool = True , not_found_text : str = "К сожалению не удалось найти информацию по юзеру",not_found_short_text = "Неизвестно"):
    async with aiosqlite.connect("user_data.db") as conn:
        try:
            cur = await conn.cursor()
            if by_short_id:
                await cur.execute("SELECT * FROM users WHERE short_id=?",(id,))
            else:
                await cur.execute("SELECT * FROM users WHERE user_own_id=?",(id,))
            user = await cur.fetchone()
            if not user:
                return not_found_text
            short_id, user_own_id, full_name, username, phone_number, country, operator, created_at = user
            text = f"ID : {user_own_id}\nПолное имя : {full_name}\n@Юзернейм : {username if username else not_found_short_text}\nНомер : {phone_number}\nСтрана : {country if country else not_found_short_text}\nСотовый оператор : {operator if operator else not_found_short_text}"
            return text
        except aiosqlite.Error as e:
            return False,e

async def add_user(new_user):
    async with aiosqlite.connect('user_data.db') as conn:
        try:
            cur = await conn.cursor()
            await cur.execute("INSERT INTO users (user_own_id,full_name,username,phone_number,country,operator) VALUES (?,?,?,?,?,?)", new_user)
            await conn.commit()
            return True
        except aiosqlite.Error as e:
            return False
        
async def get_all_users_id():
    async with aiosqlite.connect('user_data.db') as conn:
        try:
            cur = await conn.cursor()
            await cur.execute("SELECT user_own_id FROM users")
            users = await cur.fetchall()
            return users
        except aiosqlite.Error as e:
            return False
    
def search_user_info(contact : types.Contact , message : types.Message = None , return_as_list : bool = False , not_found_text = 'Неизвестно' , is_user_contact = False):
    number = contact.phone_number
    
    if not number.startswith('+'):
        number = '+' + number
    try:
        parsed_number = parse(number)
        final_number = format_number(parsed_number,PhoneNumberFormat.INTERNATIONAL)
        if not is_valid_number(parsed_number):
            parsed_number = f'Неактуален({final_number})'
            if return_as_list == True:
                return (contact.user_id, contact.full_name, message.from_user.username if is_user_contact else None, parsed_number, None, None)
            else:
                return f"ID : {contact.user_id}\nПолное имя : {contact.full_name}\nЮзернейм : @{message.from_user.username if is_user_contact else not_found_text}\nНомер : {parsed_number}\nСтрана : {not_found_text}\nСотовый оператор : {not_found_text}"
        region = geocoder.country_name_for_number(parsed_number,"ru")
        operator = carrier.name_for_number(parsed_number,"ru")
        if return_as_list == True:
            return (contact.user_id, contact.full_name, message.from_user.username if is_user_contact else None, str(final_number), region, operator)
        else:
            return f"ID : {contact.user_id}\nПолное имя : {contact.full_name}\nЮзернейм : @{message.from_user.username if is_user_contact else not_found_text}\nНомер : {final_number}\nСтрана : {region if region else not_found_text}\nСотовый оператор : {operator if operator else not_found_text}"
    except NumberParseException as e:
        return None