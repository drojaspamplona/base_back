from typing import Dict

from domain.models.auth import AuditModel
from domain.services import BaseService
from repository import BaseRepository


class AuditService(BaseService[AuditModel, None]):
    def __init__(self):
        super().__init__(BaseRepository("auth", "audit", "audit_id"))

    def __parse__(self, record: Dict) -> AuditModel:
        return AuditModel.parse_obj(record)
