from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.loans.controllers.loan_controller import LoanController
from app.modules.loans.schemas.requests import LoanCreateRequest, LoanExtendRequest
from app.modules.loans.schemas.responses import LoanResponse
from app.core.exceptions import (
    LoanNotFoundException, UserNotFoundException,
    BookNotFoundException, BookNotAvailableException,
    InvalidLoanOperationException
)

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(data: LoanCreateRequest, db: Session = Depends(get_db)):
    ctrl = LoanController(db)
    try:
        return ctrl.create(data)
    except (UserNotFoundException, BookNotFoundException) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (BookNotAvailableException, InvalidLoanOperationException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{loan_id}/return", response_model=LoanResponse)
async def return_loan(loan_id: int, db: Session = Depends(get_db)):
    ctrl = LoanController(db)
    try:
        return ctrl.return_(loan_id)
    except LoanNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidLoanOperationException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{loan_id}/extend", response_model=LoanResponse)
async def extend_loan(loan_id: int, data: LoanExtendRequest, db: Session = Depends(get_db)):
    ctrl = LoanController(db)
    try:
        return ctrl.extend(loan_id, data)
    except LoanNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidLoanOperationException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/overdue", response_model=List[LoanResponse])
async def list_overdue(db: Session = Depends(get_db)):
    return LoanController(db).list_overdue()
