from typing import Any, Dict, Optional

class BookServiceException(Exception):
    """Base exception for Book Service"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class BookNotFoundException(BookServiceException):
    """Raised when book is not found"""
    def __init__(self, book_id: int):
        super().__init__(
            message=f"Book with id {book_id} not found",
            status_code=404
        )

class BookAlreadyExistsException(BookServiceException):
    """Raised when book already exists"""
    def __init__(self, isbn: str):
        super().__init__(
            message=f"Book with ISBN {isbn} already exists",
            status_code=409
        )

class InvalidBookDataException(BookServiceException):
    """Raised when book data is invalid"""
    def __init__(self, details: Dict[str, Any]):
        super().__init__(
            message="Invalid book data provided",
            status_code=400,
            details=details
        )

class InsufficientCopiesException(BookServiceException):
    """Raised when there are insufficient copies available"""
    def __init__(self, book_id: int, requested: int, available: int):
        super().__init__(
            message=f"Insufficient copies for book {book_id}. Requested: {requested}, Available: {available}",
            status_code=400
        )

class BookNotDeletableException(BookServiceException):
    """Raised when book cannot be deleted"""
    def __init__(self, book_id: int, reason: str):
        super().__init__(
            message=f"Book {book_id} cannot be deleted: {reason}",
            status_code=400
        )
