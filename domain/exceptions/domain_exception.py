import starlette.status

from infrastructure.commons.enums.error_message import ErrorMessageKey


class DomainException(Exception):
    def __init__(self, message: ErrorMessageKey, code: starlette.status = starlette.status.HTTP_400_BAD_REQUEST):
        self.message: ErrorMessageKey = message
        self.code = code
        super().__init__(self.message)
