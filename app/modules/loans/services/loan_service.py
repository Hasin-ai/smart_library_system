from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.modules.loans.repositories.loan_repository import LoanRepository
from app.modules.loans.models.loan import Loan, LoanStatus
from app.modules.loans.schemas.requests import LoanCreateRequest, LoanExtendRequest
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.books.services.book_service import BookService
from app.core.exceptions import (
    LoanNotFoundException, UserNotFoundException,
    BookNotFoundException, BookNotAvailableException,
    InvalidLoanOperationException
)

class LoanService:
    def __init__(self, db: Session):
        self.repo = LoanRepository(db)
        self.user_repo = UserRepository(db)
        self.book_svc = BookService(db)

    def create_loan(self, data: LoanCreateRequest) -> Loan:
        if not self.user_repo.get(data.user_id):
            raise UserNotFoundException(f"User {data.user_id} not found")
        book = self.book_svc.get_book(data.book_id)
        if book.available_copies < 1:
            raise BookNotAvailableException("No copies available")
        if self.repo.get_active_for_book(data.user_id, data.book_id):
            raise InvalidLoanOperationException("User already has this book on loan")
        self.book_svc.reserve_book(data.book_id)
        dd = data.model_dump()
        dd["issue_date"] = datetime.utcnow()
        dd["status"] = LoanStatus.ACTIVE
        return self.repo.create(dd)

    def return_loan(self, loan_id: int) -> Loan:
        loan = self.repo.get(loan_id)
        if not loan:
            raise LoanNotFoundException(f"Loan {loan_id} not found")
        if loan.status != LoanStatus.ACTIVE:
            raise InvalidLoanOperationException("Loan is not active")
        update = {
            "return_date": datetime.utcnow(),
            "status": LoanStatus.RETURNED
        }
        loan = self.repo.update(loan_id, update)
        self.book_svc.return_book(loan.book_id)
        return loan

    def extend_loan(self, loan_id: int, data: LoanExtendRequest) -> Loan:
        loan = self.repo.get(loan_id)
        if not loan or loan.status != LoanStatus.ACTIVE:
            raise InvalidLoanOperationException("Loan is not active")
        if loan.extensions_count >= 2:
            raise InvalidLoanOperationException("Maximum extensions reached")
        new_due = loan.due_date + timedelta(days=data.extension_days)
        return self.repo.update(loan_id, {
            "due_date": new_due,
            "extensions_count": loan.extensions_count + 1
        })

    def get_overdue(self) -> List[Loan]:
        return self.repo.get_overdue()
