from pydantic import BaseModel


class ModuleActionModel(BaseModel):
    module_action_id: int = 0
    module_action_name: str
    key: str
    module_id: int
