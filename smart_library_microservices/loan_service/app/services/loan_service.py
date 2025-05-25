from typing import List, Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate, LoanResponse, LoanWithDetailsResponse
from app.clients.user_client import UserServiceClient
from app.clients.book_client import BookServiceClient
from app.models.loan import Loan, LoanStatus
from app.config.settings import settings
from app.core.exceptions import (
    LoanNotFoundException, LoanAlreadyExistsException,
    LoanNotActiveException, MaxExtensionsReachedException
)
from app.core.logging import logger

class LoanService:
    def __init__(self, db: Session):
        self.repository = LoanRepository(db)
        self.user_client = UserServiceClient()
        self.book_client = BookServiceClient()
    
    async def create_loan(self, loan_data: LoanCreate) -> LoanResponse:
        """Create a new loan"""
        logger.info(f"Creating loan for user {loan_data.user_id} and book {loan_data.book_id}")
        
        # Validate user exists
        user = await self.user_client.get_user(loan_data.user_id)
        logger.info(f"User {loan_data.user_id} validated")
        
        # Validate book exists and is available
        book = await self.book_client.get_book(loan_data.book_id)
        if book.get("available_copies", 0) < 1:
            logger.warning(f"Book {loan_data.book_id} not available")
            raise BookNotAvailableException(loan_data.book_id)
        logger.info(f"Book {loan_data.book_id} validated and available")
        
        # Check if user already has active loan for this book
        existing_loan = self.repository.get_active_loan(loan_data.user_id, loan_data.book_id)
        if existing_loan:
            logger.warning(f"User {loan_data.user_id} already has active loan for book {loan_data.book_id}")
            raise LoanAlreadyExistsException(loan_data.user_id, loan_data.book_id)
        
        # Create loan
        loan = self.repository.create(loan_data)
        logger.info(f"Loan {loan.id} created")
        
        # Update book availability
        try:
            await self.book_client.update_availability(loan_data.book_id, "decrement")
            logger.info(f"Book {loan_data.book_id} availability decremented")
        except Exception as e:
            # Rollback loan creation if book update fails
            logger.error(f"Failed to update book availability: {str(e)}")
            self.repository.db.delete(loan)
            self.repository.db.commit()
            raise
        
        return LoanResponse.model_validate(loan)
    
    async def return_loan(self, loan_id: int) -> LoanResponse:
        """Return a loan"""
        logger.info(f"Returning loan {loan_id}")
        
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            logger.warning(f"Loan {loan_id} not found")
            raise LoanNotFoundException(loan_id)
        
        if loan.status != LoanStatus.ACTIVE:
            logger.warning(f"Loan {loan_id} is not active")
            raise LoanNotActiveException(loan_id)
        
        # Update loan status
        loan.status = LoanStatus.RETURNED
        loan.return_date = datetime.utcnow()
        loan = self.repository.update(loan)
        logger.info(f"Loan {loan_id} marked as returned")
        
        # Update book availability
        try:
            await self.book_client.update_availability(loan.book_id, "increment")
            logger.info(f"Book {loan.book_id} availability incremented")
        except Exception as e:
            # Log error but don't rollback - loan is already returned
            logger.error(f"Failed to update book availability: {str(e)}")
        
        return LoanResponse.model_validate(loan)
    
    async def extend_loan(self, loan_id: int, extension_days: int) -> LoanResponse:
        """Extend a loan"""
        logger.info(f"Extending loan {loan_id} by {extension_days} days")
        
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            logger.warning(f"Loan {loan_id} not found")
            raise LoanNotFoundException(loan_id)
        
        if loan.status != LoanStatus.ACTIVE:
            logger.warning(f"Loan {loan_id} is not active")
            raise LoanNotActiveException(loan_id)
        
        if loan.extensions_count >= settings.MAX_EXTENSIONS:
            logger.warning(f"Loan {loan_id} has reached max extensions")
            raise MaxExtensionsReachedException(loan_id)
        
        # Extend loan
        loan.due_date = loan.due_date + timedelta(days=extension_days)
        loan.extensions_count += 1
        loan = self.repository.update(loan)
        logger.info(f"Loan {loan_id} extended to {loan.due_date}")
        
        return LoanResponse.model_validate(loan)
    
    async def get_loan(self, loan_id: int) -> LoanResponse:
        """Get loan by ID"""
        logger.info(f"Fetching loan {loan_id}")
        
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            logger.warning(f"Loan {loan_id} not found")
            raise LoanNotFoundException(loan_id)
        
        return LoanResponse.model_validate(loan)
    
    async def get_loan_with_details(self, loan_id: int) -> LoanWithDetailsResponse:
        """Get loan with user and book details"""
        logger.info(f"Fetching loan {loan_id} with details")
        
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            logger.warning(f"Loan {loan_id} not found")
            raise LoanNotFoundException(loan_id)
        
        # Fetch user and book details
        try:
            user = await self.user_client.get_user(loan.user_id)
        except Exception as e:
            logger.error(f"Failed to get user details: {str(e)}")
            user = {"id": loan.user_id, "name": "Unknown", "email": "unknown"}
        
        try:
            book = await self.book_client.get_book(loan.book_id)
        except Exception as e:
            logger.error(f"Failed to get book details: {str(e)}")
            book = {"id": loan.book_id, "title": "Unknown", "author": "Unknown"}
        
        return LoanWithDetailsResponse(
            id=loan.id,
            user=user,
            book=book,
            issue_date=loan.issue_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
            status=loan.status,
            extensions_count=loan.extensions_count,
            created_at=loan.created_at,
            updated_at=loan.updated_at
        )
    
    async def get_user_loans(self, user_id: int) -> List[LoanWithDetailsResponse]:
        """Get all loans for a user"""
        logger.info(f"Fetching loans for user {user_id}")
        
        # Validate user exists
        await self.user_client.get_user(user_id)
        
        loans = self.repository.get_user_loans(user_id)
        result = []
        
        for loan in loans:
            try:
                book = await self.book_client.get_book(loan.book_id)
            except Exception as e:
                logger.error(f"Failed to get book details: {str(e)}")
                book = {"id": loan.book_id, "title": "Unknown", "author": "Unknown"}
            
            result.append(LoanWithDetailsResponse(
                id=loan.id,
                user={"id": user_id},  # User is already validated
                book=book,
                issue_date=loan.issue_date,
                due_date=loan.due_date,
                return_date=loan.return_date,
                status=loan.status,
                extensions_count=loan.extensions_count,
                created_at=loan.created_at,
                updated_at=loan.updated_at
            ))
        
        return result
    
    def list_loans(self, page: int, per_page: int, status: Optional[LoanStatus] = None) -> Tuple[List[LoanResponse], int]:
        """List loans with pagination"""
        logger.info(f"Listing loans - page: {page}, per_page: {per_page}, status: {status}")
        
        loans, total = self.repository.list_all(page, per_page, status)
        loan_responses = [LoanResponse.model_validate(loan) for loan in loans]
        
        return loan_responses, total
    
    def get_overdue_loans(self) -> List[LoanResponse]:
        """Get all overdue loans"""
        logger.info("Fetching overdue loans")
        
        # Update overdue status
        updated = self.repository.update_overdue_status()
        if updated > 0:
            logger.info(f"Updated {updated} loans to OVERDUE status")
        
        loans = self.repository.get_overdue_loans()
        return [LoanResponse.model_validate(loan) for loan in loans]
