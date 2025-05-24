from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.shared.base_model import BaseModel

class Book(BaseModel):
    __tablename__ = "books"
    
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    genre = Column(String)
    copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    
    # Relationship to loans
    loans = relationship("Loan", back_populates="book", lazy="dynamic")
