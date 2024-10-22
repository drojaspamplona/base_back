from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from domain.models.auth.user_model import AuthUserPermissionsModel
from domain.services.auth import UserService
from infrastructure.dependencies.get_user_id_from_header import get_user_id_from_header


async def get_current_user(user_id: int = Depends(get_user_id_from_header)) -> AuthUserPermissionsModel:
    try:
        return await UserService().get_user_and_permissions_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
