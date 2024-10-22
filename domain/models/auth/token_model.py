from typing import Optional, List

from pydantic import BaseModel

from domain.models.auth.user_model import UserModel, PermissionsModel


class TokeModel(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserModel
    permissions: Optional[List[PermissionsModel]] = []
