from typing import List, Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: int = 0
    name: str
    email: str
    status: bool = True


class AuthUserModel(UserModel):
    salt: Optional[str]
    password: str


class CreateUserPermissionsModel(AuthUserModel):
    permissions: List[int]


class PermissionsModel(BaseModel):
    user_id: int
    permission: str
    module: str


class AuthUserPermissionsModel(UserModel):
    permissions: Optional[List[PermissionsModel]]
