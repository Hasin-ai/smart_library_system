from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
from app.modules.books.models.book import Book
from app.modules.users.models.user import User
from app.modules.loans.models.loan import Loan, LoanStatus
from app.modules.statistics.schemas.responses import PopularBookResponse, ActiveUserResponse, SystemOverviewResponse

class StatisticsService:
    def __init__(self, db: Session):
        self.db = db

    def popular_books(self, limit: int = 10) -> List[PopularBookResponse]:
        rows = (
            self.db.query(
                Book.id, Book.title, Book.author, func.count(Loan.id).label("borrow_count")
            )
            .join(Loan, Book.id == Loan.book_id)
            .group_by(Book.id, Book.title, Book.author)
            .order_by(func.count(Loan.id).desc())
            .limit(limit)
            .all()
        )
        return [PopularBookResponse(book_id=r.id, title=r.title, author=r.author, borrow_count=r.borrow_count) for r in rows]

    def active_users(self, limit: int = 10) -> List[ActiveUserResponse]:
        sub = (
            self.db.query(Loan.user_id, func.count(Loan.id).label("current"))
            .filter(Loan.status == LoanStatus.ACTIVE)
            .group_by(Loan.user_id)
            .subquery()
        )
        rows = (
            self.db.query(
                User.id, User.name,
                func.count(Loan.id).label("total"),
                func.coalesce(sub.c.current, 0).label("current")
            )
            .join(Loan, User.id == Loan.user_id)
            .outerjoin(sub, User.id == sub.c.user_id)
            .group_by(User.id, User.name, sub.c.current)
            .order_by(func.count(Loan.id).desc())
            .limit(limit)
            .all()
        )
        return [ActiveUserResponse(user_id=r.id, name=r.name, total_borrows=r.total, current_borrows=r.current) for r in rows]

    def overview(self) -> SystemOverviewResponse:
        total_books = self.db.query(func.count(Book.id)).scalar() or 0
        total_users = self.db.query(func.count(User.id)).scalar() or 0
        active_loans = self.db.query(func.count(Loan.id)).filter(Loan.status == LoanStatus.ACTIVE).scalar() or 0
        overdue_loans = self.db.query(func.count(Loan.id)).filter(and_(Loan.status==LoanStatus.ACTIVE, Loan.due_date<datetime.utcnow())).scalar() or 0
        available_books = self.db.query(func.sum(Book.available_copies)).scalar() or 0
        total_loans = self.db.query(func.count(Loan.id)).scalar() or 0
        return SystemOverviewResponse(
            total_books=total_books,
            total_users=total_users,
            active_loans=active_loans,
            overdue_loans=overdue_loans,
            available_books=int(available_books),
            total_loans_issued=total_loans
        )
