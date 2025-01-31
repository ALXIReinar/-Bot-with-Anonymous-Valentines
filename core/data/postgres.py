from typing import List

from asyncpg import pool, Record
from asyncpg.exceptions import SerializationError

from core.config import DEUNKNOWN_COST


class PgSql:
    """users (id, tg_id, f_name, refer_hozain, received_mes, sent_mes, refs_all_time, refs_rewards, free_deunknowns)"""
    def __init__(self, connection: pool.Pool):
        self.cursor = connection

    async def add_user(self, tg_id, first_name):
        """Добавление пользователя в БД с/без Рефкой"""
        async with self.cursor.acquire() as conn:
            query = 'INSERT INTO users (tg_id, f_name) VALUES($1,$2) ON CONFLICT (tg_id) DO UPDATE SET f_name = $2'
            await conn.execute(query, tg_id, first_name)

    async def adresat_id(self, refer):
        """Поиск владельца рефералки"""
        async with self.cursor.acquire() as conn:
            query = "SELECT f_name FROM users WHERE tg_id = $1"
            res: List[Record] =  await conn.fetch(query, refer)
            return res

    async def freebies(self, tg_id):
        """Инфа по плюшкам за Рефералов"""
        async with self.cursor.acquire() as conn:
            query = 'SELECT (refs_rewards, free_deunknowns) FROM users WHERE tg_id = $1'
            res: List[Record] = await conn.fetch(query, tg_id)
            return res

    async def statistics(self, tg_id):
        """Статистика"""
        async with self.cursor.acquire() as conn:
            query = 'SELECT (received_mes, sent_mes, refs_all_time) FROM users WHERE tg_id = $1'
            res: List[Record] = await conn.fetch(query, tg_id)
            return res

    async def check_balance_deunknown(self, tg_id):
        """Проверка наличия Деанонов"""
        not_null = True
        async with self.cursor.acquire() as conn:
            query = 'SELECT free_deunknowns FROM users WHERE tg_id = $1'

            res: List[Record] = await conn.fetch(query, tg_id)
            if not res[0][0]:
                not_null = False

            return not_null

    async def debiting_deunknowns(self, tg_id):
        """Инкриз Деанонов"""
        async with self.cursor.acquire() as conn:
            query = 'UPDATE users SET free_deunknowns = free_deunknowns - 1 WHERE tg_id = $1'
            await conn.execute(query, tg_id)


    """
    TRANSACTIONS
    """
    async def sent_receive_Transaction(self, sender, recipient):
        """Отправка-Принятие сообщений для Статистики"""
        async with self.cursor.acquire() as conn:
            async with conn.transaction(isolation='read_committed'):

                update_1 = 'UPDATE users SET sent_mes = sent_mes + 1 WHERE tg_id = $1'
                update_2 = 'UPDATE users SET received_mes = received_mes + 1 WHERE tg_id = $1'
                await conn.execute(update_1, sender)
                await conn.execute(update_2, recipient)



    async def check_user_Transaction(self, tg_id, conn):
        """Проверка пользователя на наличие БД"""
        query = "SELECT count(id) FROM users WHERE tg_id = $1"
        res: List[Record] = await conn.fetch(query, tg_id)
        return res[0][0]

    async def try_referal_increase(self, tg_id, ref, f_name):
        """Новый пользователь по Реферальной ссылке"""
        async with self.cursor.acquire() as conn:
            async with conn.transaction(isolation='serializable'):
                if await self.check_user_Transaction(tg_id, conn):
                    await conn.execute('ROLLBACK')

                else:
                    try:
                        query_insert = 'INSERT INTO users (tg_id, refer_hozain, f_name) VALUES($1,$2,$3)'
                        query_update = 'UPDATE users SET referals_all_time = referals_all_time + 1, referals_rewards = referals_rewards + 1 WHERE tg_id = $1'
                        await conn.execute(query_insert, tg_id, ref, f_name)
                        await conn.execute(query_update, tg_id)

                    except SerializationError:
                        await conn.execute('ROLLBACK')
                        await self.try_referal_increase(tg_id, ref, f_name)
                    except Exception:
                        await conn.execute('ROLLBACK')

    async def ref_rewards_deunknowns_Transaction(self, tg_id, current_ref_rewards):
        """Обмен рефералов на Деаноны"""
        async with self.cursor.acquire() as conn:
            async with conn.transaction(isolation='repeatable_read'):
                res_exchange = int(current_ref_rewards) // DEUNKNOWN_COST
                on_exit = True, res_exchange
                if res_exchange == 0:
                    await conn.execute('ROLLBACK')
                    on_exit = False, res_exchange

                else:
                    try:
                        query_subtract = 'UPDATE users SET refs_rewards = refs_rewards - $1 WHERE tg_id = $2'
                        query_add = 'UPDATE users SET free_deunknowns = free_deunknowns + $1 WHERE tg_id = $2'
                        await conn.execute(query_subtract, res_exchange * DEUNKNOWN_COST, tg_id)
                        await conn.execute(query_add, res_exchange, tg_id)

                    except SerializationError:
                        await conn.execute('ROLLBACK')
                        current_ref_rewards = int(current_ref_rewards) - res_exchange * DEUNKNOWN_COST
                        await self.ref_rewards_deunknowns_Transaction(tg_id, current_ref_rewards)

                return on_exit
