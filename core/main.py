import asyncio

from aiogram import Dispatcher, F
from aiogram.filters import Command

from core.data.postgres import PgSql
from core.middleware.pg_middleware import PostgresMiddleware
from core.callback_main import call_pay
from core.subcore import on_startup, helping, start
from core.app_essence import unknown_mes, pay
from core.app_essence.unknown_mes_with_photo import media_handler
from core.app_essence.statistic_rewards import my_stats, ref_rewards
from utils.state_machine import SaveSteps
from core.config import pool_settings, bot


dp = Dispatcher()


async def main():
    connection = await pool_settings()
    "Миддлвари"
    dp.update.middleware.register(PostgresMiddleware(connection))

    "Команды"
    dp.message.register(start, Command(commands='start'))
    dp.message.register(pay.accept_pay,  F.successful_payment)
    dp.pre_checkout_query.register(pay.accepting)
    dp.message.register(my_stats, Command(commands='my_stats'))
    dp.message.register(ref_rewards, Command(commands='ref_rewards'))
    dp.message.register(helping, Command(commands='help'))

    "Основной рабочий блок"
    dp.message.register(unknown_mes.anonim_mes_Command, Command(commands='anonim_message'))
    dp.message.register(unknown_mes.command_anonim_message, SaveSteps.COMMAND_ANONIM_MESSAGE)
    dp.message.register(unknown_mes.get_message_2, SaveSteps.GET_UNK_MESSAGE)
    dp.message.register(media_handler, SaveSteps.MEDIA_HANDLER)
    dp.message.register(unknown_mes.get_alias, SaveSteps.GET_ALIAS)
    dp.message.register(unknown_mes.get_confirm, SaveSteps.GET_CONFIRM)

    "Колл-беки"
    dp.callback_query.register(call_pay)

    dp.startup.register(on_startup)
    await dp.start_polling(bot,
                           db=PgSql(connection))


if __name__ == '__main__':
    asyncio.run(main())
