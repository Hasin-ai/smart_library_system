from pydantic import BaseModel
from typing import Optional

class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    copies: int = 1

class BookUpdateRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    copies: Optional[int] = None
    available_copies: Optional[int] = None
