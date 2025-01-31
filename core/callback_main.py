from aiogram.types import CallbackQuery

from core.app_essence.pay import pay_window, accept_pay
from core.app_essence.statistic_rewards import exchange_refs
from core.config import bot
from core.data.postgres import PgSql


async def call_pay(call: CallbackQuery, db: PgSql):
    chat_id = call.message.chat.id
    mes_id = call.message.message_id

    if '&' in call.data:
        await pay_window(bot, call)
    elif '*' in call.data:
        await accept_pay(call, db)
    elif call.data == 'cancel':
        await bot.delete_message(chat_id, message_id=mes_id)
        await call.message.answer('Отменено')

    elif 'exchange' in call.data:
        await bot.delete_message(chat_id, message_id=mes_id)
        await exchange_refs(call, db)

    await call.answer()