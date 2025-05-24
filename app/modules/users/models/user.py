from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from app.shared.base_model import BaseModel
import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    ADMIN = "admin"

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    
    # Relationship to loans
    loans = relationship("Loan", back_populates="user", lazy="dynamic")
