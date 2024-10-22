from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from domain.models.auth import AuthUserPermissionsModel
from domain.providers.token_provider import TokenProvider

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_user(token: str = Depends(oauth2_scheme)) -> AuthUserPermissionsModel:
    try:
        user = await TokenProvider().validate(token)
        return user
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
