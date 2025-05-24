from pydantic import BaseModel
from datetime import datetime

class LoanCreateRequest(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class LoanExtendRequest(BaseModel):
    extension_days: int = 7
