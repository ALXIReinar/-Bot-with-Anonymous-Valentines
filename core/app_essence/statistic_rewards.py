from aiogram.types import Message, CallbackQuery

from core.config import STATS, DEUNKNOWN_COST
from core.data.postgres import PgSql
from core.utils.keyboards import kb_de_unknowns


async def my_stats(message: Message, db: PgSql):
    r = await db.statistics(message.chat.id)
    received_mes, sent, referals = r[0][0]
    await message.answer(STATS.format(received_mes, referals, sent))


async def ref_rewards(message: Message, db: PgSql):
    info = await db.freebies(message.chat.id)
    unused_refs, de_unknowns = info[0][0]

    await message.answer(
        "Твои <i><b>Рефералы</b></i>👤 и бесплатные <i><b>Деаноны</b></i>🫣\n\n"
             f"За каждых <i><b>{DEUNKNOWN_COST}-х</b></i> Рефералов можно получить <b><i>Деанон</i></b>",
        reply_markup=kb_de_unknowns(unused_refs, de_unknowns))


async def exchange_refs(call: CallbackQuery, db: PgSql):
    current_ref_rewards = call.data.split('_')[-1]

    reply = 'Недостаточно рефералов к обмену😞'
    outcome, count_deunknowns = await db.ref_rewards_deunknowns_Transaction(call.message.chat.id, current_ref_rewards)

    if outcome:
        reply = f'Обменено на +{count_deunknowns} Деанонов!'
    await call.message.answer(reply)
