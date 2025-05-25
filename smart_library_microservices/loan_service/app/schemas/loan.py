from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.models.loan import LoanStatus

class LoanBase(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class LoanCreate(LoanBase):
    pass

class LoanReturn(BaseModel):
    loan_id: int

class LoanExtend(BaseModel):
    extension_days: Optional[int] = Field(7, ge=1, le=30)

class LoanResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus
    extensions_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LoanWithDetailsResponse(BaseModel):
    id: int
    user: Dict[str, Any]
    book: Dict[str, Any]
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus
    extensions_count: int
    created_at: datetime
    updated_at: datetime

class UserLoansResponse(BaseModel):
    loans: List[LoanWithDetailsResponse]
    total: int

class LoanListResponse(BaseModel):
    loans: List[LoanResponse]
    total: int
    page: int
    per_page: int

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    database: str
    user_service: str
    book_service: str
    timestamp: datetime
