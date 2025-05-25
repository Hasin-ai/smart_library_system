from typing import Any, Dict, Optional

class LoanServiceException(Exception):
    """Base exception for Loan Service"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class LoanNotFoundException(LoanServiceException):
    """Raised when loan is not found"""
    def __init__(self, loan_id: int):
        super().__init__(
            message=f"Loan with id {loan_id} not found",
            status_code=404
        )

class UserNotFoundException(LoanServiceException):
    """Raised when user is not found"""
    def __init__(self, user_id: int):
        super().__init__(
            message=f"User with id {user_id} not found",
            status_code=404
        )

class BookNotFoundException(LoanServiceException):
    """Raised when book is not found"""
    def __init__(self, book_id: int):
        super().__init__(
            message=f"Book with id {book_id} not found",
            status_code=404
        )

class BookNotAvailableException(LoanServiceException):
    """Raised when book is not available"""
    def __init__(self, book_id: int):
        super().__init__(
            message=f"Book with id {book_id} is not available",
            status_code=400
        )

class LoanAlreadyExistsException(LoanServiceException):
    """Raised when user already has active loan for book"""
    def __init__(self, user_id: int, book_id: int):
        super().__init__(
            message=f"User {user_id} already has an active loan for book {book_id}",
            status_code=409
        )

class LoanNotActiveException(LoanServiceException):
    """Raised when operation requires active loan"""
    def __init__(self, loan_id: int):
        super().__init__(
            message=f"Loan {loan_id} is not active",
            status_code=400
        )

class MaxExtensionsReachedException(LoanServiceException):
    """Raised when max extensions reached"""
    def __init__(self, loan_id: int):
        super().__init__(
            message=f"Loan {loan_id} has reached maximum extensions",
            status_code=400
        )

class ServiceUnavailableException(LoanServiceException):
    """Raised when external service is unavailable"""
    def __init__(self, service: str):
        super().__init__(
            message=f"{service} is unavailable",
            status_code=503
        )
