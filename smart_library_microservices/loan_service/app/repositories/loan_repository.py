from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime
from app.models.loan import Loan, LoanStatus
from app.schemas.loan import LoanCreate

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, loan_data: LoanCreate) -> Loan:
        """Create a new loan"""
        loan = Loan(
            user_id=loan_data.user_id,
            book_id=loan_data.book_id,
            due_date=loan_data.due_date,
            status=LoanStatus.ACTIVE
        )
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan
    
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        """Get loan by ID"""
        return self.db.query(Loan).filter(Loan.id == loan_id).first()
    
    def get_active_loan(self, user_id: int, book_id: int) -> Optional[Loan]:
        """Get active loan for user and book"""
        return self.db.query(Loan).filter(
            and_(
                Loan.user_id == user_id,
                Loan.book_id == book_id,
                Loan.status == LoanStatus.ACTIVE
            )
        ).first()
    
    def update(self, loan: Loan) -> Loan:
        """Update loan"""
        self.db.commit()
        self.db.refresh(loan)
        return loan
    
    def get_user_loans(self, user_id: int, active_only: bool = False) -> List[Loan]:
        """Get loans for a user"""
        query = self.db.query(Loan).filter(Loan.user_id == user_id)
        if active_only:
            query = query.filter(Loan.status == LoanStatus.ACTIVE)
        return query.order_by(Loan.issue_date.desc()).all()
    
    def get_book_loans(self, book_id: int, active_only: bool = False) -> List[Loan]:
        """Get loans for a book"""
        query = self.db.query(Loan).filter(Loan.book_id == book_id)
        if active_only:
            query = query.filter(Loan.status == LoanStatus.ACTIVE)
        return query.order_by(Loan.issue_date.desc()).all()
    
    def get_overdue_loans(self) -> List[Loan]:
        """Get all overdue loans"""
        now = datetime.utcnow()
        return self.db.query(Loan).filter(
            and_(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date < now
            )
        ).all()
    
    def list_all(self, page: int, per_page: int, status: Optional[LoanStatus] = None) -> Tuple[List[Loan], int]:
        """List loans with pagination"""
        query = self.db.query(Loan)
        
        if status:
            query = query.filter(Loan.status == status)
        
        total = query.count()
        loans = query.order_by(Loan.issue_date.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        return loans, total
    
    def count_active_loans(self) -> int:
        """Count active loans"""
        return self.db.query(func.count(Loan.id)).filter(Loan.status == LoanStatus.ACTIVE).scalar()
    
    def update_overdue_status(self) -> int:
        """Update status of overdue loans"""
        now = datetime.utcnow()
        result = self.db.query(Loan).filter(
            and_(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date < now
            )
        ).update({Loan.status: LoanStatus.OVERDUE})
        self.db.commit()
        return result
