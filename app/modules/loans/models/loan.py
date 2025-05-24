from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.shared.base_model import BaseModel
import enum
from datetime import datetime

class LoanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

class Loan(BaseModel):
    __tablename__ = "loans"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    extensions_count = Column(Integer, default=0)

    # Relationships using string references to avoid circular imports
    user = relationship("User", back_populates="loans", lazy="select")
    book = relationship("Book", back_populates="loans", lazy="select")
