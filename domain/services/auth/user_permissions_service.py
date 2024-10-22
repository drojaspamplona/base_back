from itertools import groupby
from typing import Dict, List, NoReturn

from domain.models.auth import UserPermissionsModel
from domain.models.auth.user_permissions_model import PermissionsNodeModel, VwUserPermission, ChildPermissionsNodeModel
from domain.services import BaseService
from domain.services.auth.module_service import ModuleService
from repository.auth import UserPermissionsRepository


class UserPermissionsService(BaseService[UserPermissionsModel, UserPermissionsRepository]):
    def __init__(self):
        super().__init__(UserPermissionsRepository())
        self.module_service = ModuleService()

    def __parse__(self, record: Dict) -> UserPermissionsModel:
        return UserPermissionsModel.parse_obj(record)

    async def get_permissions_node(self, user_id: int) -> List[PermissionsNodeModel]:
        response: List[PermissionsNodeModel] = []
        module_permissions = await self.module_service.get_module_actions()
        user_permissions = await self.get_user_permissions(user_id) if user_id else []
        for key, group in groupby(module_permissions, lambda x: x.module_id):
            module = next((mod for mod in module_permissions if mod.module_id == key), "none")
            if module != "none":
                children = [ChildPermissionsNodeModel(title=g.module_action_name, key=str(g.module_action_key),
                                                      id=g.module_action_id,
                                                      checked=self.__check_permission__(user_permissions,
                                                                                        g.module_action_id)) for g in
                            group]
                header = PermissionsNodeModel(title=module.module_name, key=module.module_key, id=module.module_id,
                                              children=children)
                response.append(header)
        return response

    async def get_user_permissions(self, user_id: int) -> List[VwUserPermission]:
        records = await self.repository.get_user_permissions(user_id)
        return self.__parse_all_custom__(records, VwUserPermission)

    async def add_user_permissions(self, user_id: int, permissions: List[int]) -> NoReturn:
        for p in permissions:
            await self.create(UserPermissionsModel(user_id=user_id, module_action_id=p))

    async def update_user_permissions(self, user_id: int, permissions: List[int]) -> NoReturn:
        await self.repository.delete_all_user_permissions(user_id)
        for p in permissions:
            await self.create(UserPermissionsModel(user_id=user_id, module_action_id=p))

    def __check_permission__(self, permissions: List[VwUserPermission], module_action_id: int) -> bool:
        return module_action_id in [p.module_action_id for p in permissions]
