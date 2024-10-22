from typing import Dict, List

from domain.models.auth import ModuleModel
from domain.models.auth.module_model import VwModuleActions
from domain.services import BaseService
from repository.auth import ModuleRepository


class ModuleService(BaseService[ModuleModel, ModuleRepository]):
    def __init__(self):
        super().__init__(ModuleRepository())

    def __parse__(self, record: Dict) -> ModuleModel:
        return ModuleModel.parse_obj(record)

    async def get_module_actions(self) -> List[VwModuleActions]:
        records = await self.repository.get_module_actions()
        return self.__parse_all_custom__(records, VwModuleActions)
