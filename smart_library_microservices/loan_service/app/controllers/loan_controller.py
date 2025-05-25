from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.services.loan_service import LoanService
from app.schemas.loan import (
    LoanCreate, LoanReturn, LoanExtend, LoanResponse,
    LoanWithDetailsResponse, UserLoansResponse, LoanListResponse
)
from app.models.loan import LoanStatus
from app.core.exceptions import LoanServiceException
from app.core.logging import logger

router = APIRouter(prefix="/api/loans", tags=["loans"])

@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
) -> LoanResponse:
    """Create a new loan"""
    try:
        service = LoanService(db)
        return await service.create_loan(loan_data)
    except LoanServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error creating loan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/returns", response_model=LoanResponse)
async def return_loan(
    return_data: LoanReturn,
    db: Session = Depends(get_db)
) -> LoanResponse:
    """Return a loan"""
    try:
        service = LoanService(db)
        return await service.return_loan(return_data.loan_id)
    except LoanServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error returning loan: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{loan_id}/extend", response_model=LoanResponse)
async def extend_loan(
    loan_id: int,
    extend_data: LoanExtend,
    db: Session = Depends(get_db)
) -> LoanResponse:
    """Extend a loan"""
    try:
        service = LoanService(db)
        return await service.extend_loan(loan_id, extend_data.extension_days)
    except LoanServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error extending loan {loan_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{loan_id}", response_model=LoanWithDetailsResponse)
async def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
) -> LoanWithDetailsResponse:
    """Get loan details"""
    try:
        service = LoanService(db)
        return await service.get_loan_with_details(loan_id)
    except LoanServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error fetching loan {loan_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}", response_model=UserLoansResponse)
async def get_user_loans(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserLoansResponse:
    """Get loans for a user"""
    try:
        service = LoanService(db)
        loans = await service.get_user_loans(user_id)
        return UserLoansResponse(loans=loans, total=len(loans))
    except LoanServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error fetching loans for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("", response_model=LoanListResponse)
async def list_loans(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    status: Optional[LoanStatus] = Query(None),
    db: Session = Depends(get_db)
) -> LoanListResponse:
    """List loans with pagination"""
    try:
        service = LoanService(db)
        loans, total = service.list_loans(page, per_page, status)
        
        return LoanListResponse(
            loans=loans,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        logger.error(f"Unexpected error listing loans: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/overdue", response_model=list[LoanResponse])
async def get_overdue_loans(
    db: Session = Depends(get_db)
) -> list[LoanResponse]:
    """Get all overdue loans"""
    try:
        service = LoanService(db)
        return service.get_overdue_loans()
    except Exception as e:
        logger.error(f"Unexpected error fetching overdue loans: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
