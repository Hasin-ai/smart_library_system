from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    genre: Optional[str]
    copies: int
    available_copies: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
