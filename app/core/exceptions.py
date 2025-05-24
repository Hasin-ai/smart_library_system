class LibraryException(Exception):
    pass

class UserAlreadyExistsException(LibraryException):
    pass

class UserNotFoundException(LibraryException):
    pass

class BookAlreadyExistsException(LibraryException):
    pass

class BookNotFoundException(LibraryException):
    pass

class BookNotAvailableException(LibraryException):
    pass

class LoanNotFoundException(LibraryException):
    pass

class InvalidLoanOperationException(LibraryException):
    pass
