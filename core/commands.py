from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/anonim_message', description='Написать анонимное сообщение'),
        BotCommand(command='/my_stats', description='Статистика аккаунта'),
        BotCommand(command='/ref_rewards', description='Бонусы за приведённых людей'),
        BotCommand(command='/help', description='Ответы на частые вопросы')
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
