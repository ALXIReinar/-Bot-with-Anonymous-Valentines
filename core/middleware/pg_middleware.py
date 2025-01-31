from asyncpg import pool
from typing import Any, Callable, Dict, Awaitable

from aiogram.types import TelegramObject
from aiogram import BaseMiddleware

from core.data.postgres import PgSql


class PostgresMiddleware(BaseMiddleware):
    def __init__(self, connection: pool.Pool):
        super().__init__()
        self.connection = connection

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> None:
        async with self.connection.acquire() as conn:
            data['psql_connection'] = PgSql(conn)
            return await handler(event, data)
