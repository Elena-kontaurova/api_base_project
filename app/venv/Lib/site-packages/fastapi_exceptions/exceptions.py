from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class ValidationError(HTTPException):
    def __init__(
        self,
        detail: Any = 'Invalid input',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.headers = headers


class NotAuthenticated(HTTPException):
    def __init__(
        self,
        detail: Any = 'Authentication credentials were not provided',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers


class AuthenticationFailed(HTTPException):
    def __init__(
        self,
        detail: Any = 'Incorrect authentication credentials',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = headers


class PermissionDenied(HTTPException):
    def __init__(
        self,
        detail: Any = 'You do not have permission to perform this action',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        self.headers = headers


class NotFound(HTTPException):
    def __init__(
        self,
        detail: Any = 'Not found',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        self.headers = headers
