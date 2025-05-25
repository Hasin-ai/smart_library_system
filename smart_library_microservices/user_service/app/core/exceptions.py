from typing import Any, Dict, Optional

class UserServiceException(Exception):
    """Base exception for User Service"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class UserNotFoundException(UserServiceException):
    """Raised when user is not found"""
    def __init__(self, user_id: int):
        super().__init__(
            message=f"User with id {user_id} not found",
            status_code=404
        )

class UserAlreadyExistsException(UserServiceException):
    """Raised when user already exists"""
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email {email} already exists",
            status_code=409
        )

class InvalidUserDataException(UserServiceException):
    """Raised when user data is invalid"""
    def __init__(self, details: Dict[str, Any]):
        super().__init__(
            message="Invalid user data provided",
            status_code=400,
            details=details
        )
