import json

import redis

from config import settings
from domain.exceptions import DomainException
from domain.models.auth import UserModel, UserPermissionsModel
from infrastructure.commons.enums.error_message import ErrorMessageKey


class RedisProvider:
    def __init__(self):
        config = settings.redis_config
        self.r = redis.Redis(host=config.host, port=config.port, db=config.db, ssl=config.ssl, encoding='utf-8',
                             socket_timeout=1)

    def save_user(self, user: UserModel, user_permissions: UserPermissionsModel):
        self.r.set(f"{user.user_id}_user", json.dumps(user.dict()))
        self.r.set(f"{user.user_id}_user_permissions", json.dumps(user_permissions.dict()))

    def get_user(self, user_id: int) -> UserModel:
        user = self.r.get(f"{user_id}_user")
        if user:
            user_dict = json.loads(user)
            return UserModel(**user_dict)
        raise DomainException(ErrorMessageKey.UNAUTHORIZED, 401)

    def get_user_permissions(self, user_id: int) -> UserPermissionsModel:
        user_permissions = self.r.get(f"{user_id}_user_permissions")
        if user_permissions:
            user_user_permissions_dict = json.loads(user_permissions)
            return UserPermissionsModel(**user_user_permissions_dict)
        raise DomainException(ErrorMessageKey.UNAUTHORIZED, 401)
