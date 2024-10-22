from fastapi import HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from domain.providers.token_provider import TokenProvider


async def get_user_id_from_header(request: Request) -> int:
    try:
        authorization: str = request.headers.get("authorization")
        if authorization:
            token = authorization.split(" ")[1]
            user = await TokenProvider().validate(token)
            return user.user_id
        raise Exception("Could not validate credentials")
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
