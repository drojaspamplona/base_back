from typing import List

from fastapi import APIRouter, Depends

from domain.models.auth import LoginModel, UserModel
from domain.models.auth import TokeModel
from domain.models.auth.user_model import CreateUserPermissionsModel
from domain.models.auth.user_permissions_model import PermissionsNodeModel
from domain.services.auth import UserService, UserPermissionsService
from infrastructure.dependencies.auth_request import AuthRequest

router = APIRouter()


@router.post("/login", response_model=TokeModel)
async def login(request: LoginModel, service: UserService = Depends()):
    return await service.login(request.user_name, request.password)


@router.post("/", response_model=UserModel, dependencies=[Depends(AuthRequest(p=["users:create"]))])
async def create(request: CreateUserPermissionsModel, service: UserService = Depends()):
    return await service.create_user(request)


@router.get("/", response_model=List[UserModel]) #dependencies=[Depends(AuthRequest(p=["users:read"]))])
async def get_all(service: UserService = Depends()):
    return await service.get_all()


@router.put("/", response_model=bool, dependencies=[Depends(AuthRequest(p=["users:update"]))])
async def update(request: CreateUserPermissionsModel, service: UserService = Depends()):
    return await service.update_user(request)


@router.get("/get-detail/{user_id}", response_model=UserModel, dependencies=[Depends(AuthRequest(p=["users:update"]))])
async def get_detail(user_id: int, service: UserService = Depends()):
    return await service.get_by_id(user_id)


@router.get("/permissions/{user_id}", response_model=List[PermissionsNodeModel],
            dependencies=[Depends(AuthRequest(p=["users:update", "users:create"]))])
async def get_permissions(user_id: int, service: UserPermissionsService = Depends()):
    return await service.get_permissions_node(user_id)
