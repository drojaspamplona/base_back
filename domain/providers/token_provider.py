import jwt
from fastapi import HTTPException
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from config import settings
from domain.models.auth import AuthUserPermissionsModel
from domain.services.auth import UserService


class TokenProvider:
    def __init__(self):
        self.config = settings.jwt_config
        self.user_service = UserService()

    async def validate(self, token: str) -> AuthUserPermissionsModel:
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
        except PyJWTError:
            raise credentials_exception
        user = await self.user_service.get_user_and_permissions_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user
