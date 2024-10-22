from typing import List, Optional

from pydantic import BaseModel


class UserPermissionsModel(BaseModel):
    user_permissions_id: int = 0
    user_id: int
    module_action_id: int


class VwUserPermission(UserPermissionsModel):
    module_action_key: str
    module_action_name: str
    module_name: str
    module_id: int
    module_key: str


# We need to do this cause FastApi don't work with the __future__ annotations
class ChildPermissionsNodeModel(BaseModel):
    title: str
    key: str
    id: int
    checked: bool = False


class PermissionsNodeModel(BaseModel):
    title: str
    key: str
    id: int
    checked: bool = False
    children: Optional[List[ChildPermissionsNodeModel]]
