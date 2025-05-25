from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

class AvailabilityOperation(str, Enum):
    INCREMENT = "increment"
    DECREMENT = "decrement"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=1, max_length=20)
    genre: Optional[str] = Field(None, max_length=100)
    copies: int = Field(1, ge=1)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=1, max_length=20)
    genre: Optional[str] = Field(None, max_length=100)
    copies: Optional[int] = Field(None, ge=1)

class BookAvailabilityUpdate(BaseModel):
    available_copies: Optional[int] = Field(None, ge=0)
    operation: Optional[AvailabilityOperation] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "operation": "decrement",
                "available_copies": None
            }
        }
    )

class BookResponse(BookBase):
    id: int
    available_copies: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class BookSearchResponse(BaseModel):
    books: List[BookResponse]
    total: int
    page: int
    per_page: int

class BookAvailabilityResponse(BaseModel):
    id: int
    available_copies: int
    updated_at: datetime

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    database: str
    timestamp: datetime
