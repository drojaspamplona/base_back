from typing import Dict

from domain.models.auth import ModuleActionModel
from domain.services import BaseService
from repository import BaseRepository


class ModuleActionService(BaseService[ModuleActionModel, None]):
    def __init__(self):
        super().__init__(BaseRepository("auth", "module_action", "module_action_id"))

    def __parse__(self, record: Dict) -> ModuleActionModel:
        return ModuleActionModel.parse_obj(record)
