from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from datetime import datetime
from app.shared.base_repository import BaseRepository
from app.modules.loans.models.loan import Loan, LoanStatus

class LoanRepository(BaseRepository[Loan]):
    def __init__(self, db: Session):
        super().__init__(Loan, db)

    def get_active_for_book(self, user_id: int, book_id: int) -> Optional[Loan]:
        return self.db.query(Loan).filter(and_(
            Loan.user_id == user_id,
            Loan.book_id == book_id,
            Loan.status == LoanStatus.ACTIVE
        )).first()

    def get_overdue(self) -> List[Loan]:
        now = datetime.utcnow()
        return self.db.query(Loan).options(joinedload(Loan.user), joinedload(Loan.book)).filter(
            Loan.status == LoanStatus.ACTIVE,
            Loan.due_date < now
        ).all()
