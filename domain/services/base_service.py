from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Generic, List, Optional, Tuple, Any, Union, Type

from pydantic import BaseModel

from repository.base_repository import BaseRepository

T = TypeVar('T')
TR = TypeVar('TR')
OT = TypeVar('OT')
Params = Tuple[Any]


class BaseService(ABC, Generic[T, TR]):
    def __init__(self, repository: Union[BaseRepository, TR]):
        self.repository: Union[BaseRepository, TR] = repository

    async def get_all(self) -> List[T]:
        results = await self.repository.get_all()
        return self.__parse_all__(results)

    async def create(self, model) -> Union[int, str]:
        return await self.repository.create(model)

    async def update(self, model) -> bool:
        await self.repository.update(model)
        return True

    async def get_by_id(self, entity_id: Union[int, str]) -> Optional[T]:
        result = await self.repository.get_by_id(entity_id)
        if result:
            return self.__parse__(result)
        return None

    @abstractmethod
    def __parse__(self, record: Dict) -> T:
        pass

    def __parse_all__(self, records: List[Dict]) -> List[T]:
        return [self.__parse__(r) for r in records]

    def __parse_all_custom__(self, records: List[Dict], model: Type[Union[BaseModel, OT]]) -> List[OT]:
        return [model.parse_obj(r) for r in records]
