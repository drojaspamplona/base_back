import base64
import json

import requests
from requests import request

from config import settings
from domain.contracts import PuaUserContract
from domain.exceptions import DomainException
from infrastructure.commons.enums.error_message import ErrorMessageKey


class PuaProvider:
    def __init__(self):
        self.config = settings.pua_config

    async def authenticate(self, user_name: str, password: str) -> PuaUserContract:
        password_bytes = password.encode("ascii")
        req = requests.post(f"{self.config.endpoint}{self.config.auth_url}",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps({"nombre": user_name,
                                             "contrasena": base64.b64encode(password_bytes).decode("ascii"),
                                             "codigoAplicacion": self.config.app_id}))
        response = await self.__get_response__(req)
        return PuaUserContract.parse_obj(response["Entidad"]["Usuario"])

    async def validate(self, token: str) -> PuaUserContract:
        req = requests.get(f"{self.config.endpoint}/{self.config.validate_token_url}",
                           params={"token": token})
        response = await self.__get_response__(req)
        return PuaUserContract.parse_obj(response["Entidad"]["Usuario"])

    async def __get_response__(self, req: request):
        if req.ok:
            response = req.json()
            if "Exitoso" not in response or not response["Exitoso"]:
                raise DomainException(ErrorMessageKey.PUA_ERROR, 401)

            if "Entidad" not in response or "Usuario" not in response["Entidad"]:
                raise DomainException(ErrorMessageKey.PUA_ERROR)
        else:
            raise DomainException(ErrorMessageKey.PUA_ERROR)
        return response
