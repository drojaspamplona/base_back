from typing import Dict, List, Optional, Tuple, Any

from pydantic import BaseModel
from six import string_types
from typing_extensions import NoReturn

from infrastructure.utils.query import build_insert, build_update
from repository.data import PostgresDb

Params = Tuple[Any, ...]


class BaseRepository:
    def __init__(self, schema: str, table_name: str, primary_key: str, omit_key: bool = True,
                 db: PostgresDb = PostgresDb()):
        self.db = db
        self.schema = schema
        self.table_name = table_name
        self.primary_key = primary_key
        self.omit_key = omit_key

    # def apply_template(self, template: str, parameters: Dict):
    #    j = JinjaSql(param_style='pyformat')
    #    query, bind_params = j.prepare_query(template, parameters)
    #    return self.__get_sql_from_template__(query, bind_params)

    # def __get_sql_from_template__(self, query: str, bind_params):
    #    if not bind_params:
    #        return query
    #    params = deepcopy(bind_params)
    #    for key, val in params.items():
    #        params[key] = self.__quote_sql_string__(val)
    #    return query % params

    def __quote_sql_string__(self, value):
        """
            If `value` is a string type, escapes single quotes in the string
            and returns the string enclosed in single quotes.
        """
        if isinstance(value, string_types):
            new_value = str(value)
            new_value = new_value.replace("'", "''")
            return "'{}'".format(new_value)
        return value

    def build_select(self):
        return f"select * from {self.schema}.{self.table_name}"

    def build_delete(self):
        return f"delete from {self.schema}.{self.table_name}"

    async def get_all(self) -> List[Dict]:
        """
        Builds and execute the select DML command for the specific entity
        :return: All the elements contained in the entity table
        """
        return await self.db.execute(self.build_select())

    async def get_by_id(self, entity_id: int) -> Dict:
        """
        Builds and execute a select command with a WHERE condition where the value is the entity id
        :param entity_id: The entity id value
        :return: A dict with the record values
        """
        return await self.db.get_first(f"select * from {self.schema}.{self.table_name} where {self.primary_key} = %s",
                                       (entity_id,))

    def parse_model_list(self, model: List[BaseModel]) -> Tuple[str, List[Tuple]]:
        params_list = []
        query = None
        for m in model:
            q, params = build_insert(m, self.primary_key, f"{self.schema}.{self.table_name}", self.omit_key)
            params_list.append(params)
            query = q
        return query, params_list

    async def create(self, model: BaseModel) -> int:
        """
        Builds and execute a create query of the entity
        :param model: The entity model
        :return: The last generated id
        """
        query, params = build_insert(model, self.primary_key, f"{self.schema}.{self.table_name}", self.omit_key)
        new_record = await self.db.insert(query, params)
        return new_record[self.primary_key] if new_record else None

    async def update(self, model: BaseModel) -> NoReturn:
        query, params = build_update(model, self.primary_key, f"{self.schema}.{self.table_name}")
        await self.db.execute_non_query(query, params)

    async def execute(self, query: str, params: Optional[Params]) -> List[Dict]:
        return await self.db.execute(query, params)

    async def execute_values(self, model: List[BaseModel]) -> NoReturn:
        query, params = self.parse_model_list(model)
        await self.db.execute_values(query, params)

    async def execute_non_query(self, query: str, params: Optional[Params]) -> NoReturn:
        return await self.db.execute_non_query(query, params)

    async def get_one(self, query: str, params: Optional[Params]) -> Dict:
        return await self.db.get_first(query, params)
