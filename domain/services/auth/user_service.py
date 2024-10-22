from typing import Dict, List

from domain.models.auth import UserModel, TokeModel
# from domain.providers.redis_provider import RedisProvider
from domain.models.auth.user_model import AuthUserModel, CreateUserPermissionsModel, AuthUserPermissionsModel, \
    PermissionsModel
from domain.providers.auth_provider import AuthProvider
from domain.services.auth.user_permissions_service import UserPermissionsService
from domain.services.base_service import BaseService
from repository.auth import UserRepository


class UserService(BaseService[UserModel, UserRepository]):
    def __init__(self):
        super().__init__(UserRepository())
        self.auth_provider = AuthProvider()
        self.user_permissions_service = UserPermissionsService()
        # self.cache_provider = RedisProvider()

    async def authenticate_user(self, user_name: str, password: str) -> TokeModel:
        """
        Authenticate the user through the PUA server
        :param user_name: The user account name
        :param password: The user password
        :return: The user information and the access token
        """
        user = await self.auth_provider.authenticate(user_name, password)
        return TokeModel(access_token=self.auth_provider.create_access_token({"user_id": user.user_id}),
                         user=UserModel(user_id=user.user_id, name=user.name.title(), email=user.email,
                                        status=user.status))

    async def login(self, user_name: str, password: str) -> TokeModel:
        """
        Authenticate the user through the PUA server and create the user if not exist in the local DB
        :param user_name: The user account name
        :param password: The user password
        :return: The user information and the access token
        """
        user = await self.authenticate_user(user_name, password)
        existing_user = await self.get_by_id(user.user.user_id)
        if not existing_user:
            await self.create(user.user)
        user.permissions = await self.get_user_permissions(user.user.user_id)
        return user

    async def create_user(self, model: CreateUserPermissionsModel) -> UserModel:
        salt, password = self.auth_provider.build_user_salt(model.password)
        user_id = await self.create(
            AuthUserModel(status=model.status, email=model.email, name=model.name, password=password, salt=salt))
        await self.user_permissions_service.add_user_permissions(user_id, model.permissions)
        return model

    async def update_user(self, request: CreateUserPermissionsModel) -> bool:
        user = await self.get_auth_user_by_id(request.user_id)
        if request.password != "":
            salt, password = self.auth_provider.build_user_salt(request.password)
            request.salt = salt
            request.password = password
        else:
            request.password = user.password
            request.salt = user.salt
        await self.update(AuthUserModel(status=request.status, email=request.email, user_id=request.user_id,
                                        name=request.name, password=request.password, salt=request.salt))
        await self.user_permissions_service.update_user_permissions(request.user_id, request.permissions)
        return True

    async def get_auth_user_by_id(self, user_id: int) -> AuthUserModel:
        user = await self.repository.get_auth_user_by_id(user_id)
        return AuthUserModel(**user)

    async def get_user_permissions(self, user_id: int) -> List[PermissionsModel]:
        records = await self.repository.get_user_permissions(user_id)
        return self.__parse_all_custom__(records, PermissionsModel)

    async def get_user_and_permissions_by_id(self, user_id: int) -> AuthUserPermissionsModel:
        user = await self.get_by_id(user_id)
        permissions = await self.get_user_permissions(user_id)
        return AuthUserPermissionsModel(**user.dict(), permissions=permissions)

    def __parse__(self, record: Dict) -> UserModel:
        return UserModel.parse_obj(record)
