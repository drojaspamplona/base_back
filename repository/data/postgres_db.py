from typing import Optional, Tuple, Any, List, Dict, NoReturn

from pandas import DataFrame, read_sql

from repository.data import DbFactory

Params = Tuple[Any]


class PostgresDb:
    def __init__(self):
        self.__persistence__ = DbFactory()

    async def get_as_data_frame(self, query) -> DataFrame:
        return read_sql(query, await self.__persistence__.connect())

    async def execute(self, query: str, params: Optional[Params] = None) -> List[Dict]:
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchall()

    async def execute_many_non_query(self, query: str, params: List[Params]) -> NoReturn:
        """
        Execute a non many query
        Arguments:
            query {[string]} -- Raw Query to execute
            params {[object]} -- the params
        """
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(query, params)

    async def insert(self, query: str, params: Params) -> Dict:
        """
        Execute an insert query and return the last id
        Arguments:
            query {[string]} -- Raw Query to execute
            params {[object]} -- the params
        """
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()
                return await cursor.fetchone()

    async def execute_non_query(self, query: str, params: Optional[Params] = None) -> NoReturn:
        """
        Execute a non many query
        Arguments:
            query {[string]} -- Raw Query to execute
            params {[object]} -- the params
        """
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)

    async def execute_values(self, query: str, params: List[Params]):
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(query, params)

    async def get_first(self, query: str, params: Optional[Params] = None) -> Dict:
        async with await self.__persistence__.connect() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchone()
