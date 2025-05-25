from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.config.database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), unique=True, index=True, nullable=False)
    genre = Column(String(100), nullable=True)
    copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('copies >= 0', name='check_copies_positive'),
        CheckConstraint('available_copies >= 0', name='check_available_copies_positive'),
        CheckConstraint('available_copies <= copies', name='check_available_copies_not_exceed_copies'),
    )
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, isbn={self.isbn})>"
