from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.modules.loans.models.loan import LoanStatus

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

    class Config:
        from_attributes = True
