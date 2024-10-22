from pydantic import BaseModel


class ModuleModel(BaseModel):
    module_id: int = 0
    module_name: str
    key: str


class VwModuleActions(BaseModel):
    module_action_id: int
    module_action_key: str
    module_action_name: str
    module_name: str
    module_id: int
    module_key: str
