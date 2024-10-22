from typing import List

from fastapi import Depends, BackgroundTasks, Request
from starlette.status import HTTP_403_FORBIDDEN

from domain.exceptions import DomainException
from domain.models.auth import AuthUserPermissionsModel
from domain.services.auth import AuditService
from infrastructure.commons.enums.error_message import ErrorMessageKey
from infrastructure.dependencies import get_user, audit_request


class AuthRequest:
    def __init__(self, m: List[str] = None, p: List[str] = None):
        self.modules = m if m else []
        self.permissions = p if p else []

    async def __call__(self, background_tasks: BackgroundTasks, request: Request,
                       user: AuthUserPermissionsModel = Depends(get_user), service: AuditService = Depends()):

        if len(self.modules) > 0:
            allowed_modules = []
            for m in self.modules:
                if m in [um.module for um in user.permissions]:
                    allowed_modules.append(m)
            if len(allowed_modules) == 0:
                raise DomainException(ErrorMessageKey.UNAUTHORIZED_ACTION, HTTP_403_FORBIDDEN)

        if len(self.permissions) > 0:
            allowed_permissions = []
            for p in self.permissions:
                if p in [up.permission for up in user.permissions]:
                    allowed_permissions.append(p)
            if len(allowed_permissions) == 0:
                raise DomainException(ErrorMessageKey.UNAUTHORIZED_ACTION, HTTP_403_FORBIDDEN)
        if len(self.modules) == 0 and len(self.permissions) == 0:
            raise DomainException(ErrorMessageKey.UNAUTHORIZED_ACTION, HTTP_403_FORBIDDEN)

        await audit_request(background_tasks, request, user, service)
