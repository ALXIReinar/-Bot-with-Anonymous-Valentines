
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from core.data.postgres import PgSql
from core.app_essence.unknown_mes import anonim_mes_start
from core.utils.keyboards import hyper_link_profile
from commands import set_commands
from config import START, LINK, ADMIN_ID, bot, HELP


async def on_startup():
    await bot.send_message(ADMIN_ID, 'Бот запущен!', reply_markup=ReplyKeyboardRemove())


async def start(message: Message, state: FSMContext, db: PgSql):
    id = message.chat.id
    f_name = message.from_user.first_name
    link = LINK.format(id)
    ref = int(message.text[7:]) if message.text[7:] != '' else 0

    if ref:                                 # ЕСЛИ С РЕФКОЙ
        if id == ref:
            await message.answer('Вы не можете написать анонимку самому себе)')
        else:
            await state.update_data(ref=ref)
            await db.try_referal_increase(id, ref, f_name)
            await anonim_mes_start(message, state, db)

    else:                                   # ЕСЛИ ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ
        await message.answer(START.format(f_name, link))
        await db.add_user(id, f_name)
    await set_commands(bot)


async def helping(message: Message):
    await message.answer(HELP, reply_markup=hyper_link_profile(ADMIN_ID))
