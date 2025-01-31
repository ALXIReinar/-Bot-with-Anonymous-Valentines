import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from asyncpg import create_pool
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

PAY_TOKEN = os.getenv('PAY_TOKEN')
LINK = os.getenv('LINK')

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DB = os.getenv('PG_DB')

DEUNKNOWN_COST = 3

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

async def pool_settings():
    return await create_pool(user=PG_USER,
                       password=PG_PASSWORD,
                       host=PG_HOST,
                       port=PG_PORT,
                       database=PG_DB,
                       command_timeout=60)

START = '''
Добро пожаловать, {}!
Здесь вы можете прочитать/написать анонимные сообщения по реферальным ссылкам

Кстати! а вот и Ваша)
{}
'''
STATS = '''
Рефералов за всё время              <i><b>{}</b></i> 👤
Получено сообщений                  <i><b>{}</b></i> 💌
Отправлено сообщений              <i><b>{}</b></i> ✍️
'''
HELP = '''
🔴 <b>Как я могу посмотреть отправленные и полученные сообщения?</b>

🟢 Введите в поиске по чату #полученные или  #отправленные . Так сделано, чтобы сообщения не хранились у нас ради обеспечения Вашей конфиденциальности
Таким же образом Вы Можете узнать #рассекреченные сообщения
'''