import psycopg
from psycopg.rows import dict_row

from config import settings


class DbFactory:
    def __init__(self):
        self.config = settings.db_config




    async def connect(self):
        connection_params = {
            "dbname": self.config.dbname,
            "user": self.config.user,
            "password": self.config.password,
            "host": self.config.host,
            "port": 5432,
        }
        return await psycopg.AsyncConnection.connect(**connection_params, row_factory=dict_row)
