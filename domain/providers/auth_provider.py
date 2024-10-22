import binascii
import hashlib
import os
from datetime import timedelta, datetime
from typing import Tuple

import jwt
from starlette.status import HTTP_401_UNAUTHORIZED

from config import settings
from domain.exceptions import DomainException
from domain.models.auth.user_model import AuthUserModel
from infrastructure.commons.enums.error_message import ErrorMessageKey
from repository.auth import UserRepository


class AuthProvider:
    def __init__(self):
        self.repository = UserRepository()

    def build_user_salt(self, password: str) -> Tuple[str, str]:
        return self.__hash_password__(password)

    async def authenticate(self, email: str, password: str) -> AuthUserModel:
        """
        Authenticate the user across the database
        :param email: The email
        :param password: The password
        :return: AuthUserModel
        """
        user = await self.repository.get_user_by_email(email)
        if user:
            user = AuthUserModel(**user)
        if user and user.status and self.__verify_password__(user.password, user.salt, password):
            return user
        else:
            raise DomainException(ErrorMessageKey.UNAUTHORIZED, HTTP_401_UNAUTHORIZED)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=int(settings.jwt_config.expire_time))

        to_encode.update(
            {"exp": expire, "sub": settings.jwt_config.access_token_subject})

        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_config.secret_key, algorithm=settings.jwt_config.algorithm)
        return encoded_jwt

    def __hash_password__(self, password: str) -> Tuple[str, str]:
        password = password + settings.salt_secret
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                       salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        return salt.decode('ascii'), pwd_hash.decode('ascii')

    def __verify_password__(self, stored_password: str, salt: str, password: str) -> bool:
        """
        Verify the password integrity
        :param stored_password: The stored password
        :param salt: The stored salt
        :param password: The password included in the auth request
        :return:
        """
        password = password + settings.salt_secret
        pwd_hash = hashlib.pbkdf2_hmac('sha512',
                                       password.encode('utf-8'),
                                       salt.encode('ascii'),
                                       100000)
        pwd_hash_save = binascii.hexlify(pwd_hash).decode('ascii')
        return pwd_hash_save == stored_password
