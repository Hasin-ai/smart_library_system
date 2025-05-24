#!/usr/bin/env python3
"""Initialize database tables"""
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.database import engine
from app.shared.base_model import Base
# Import all models to register them
from app.modules.users.models.user import User
from app.modules.books.models.book import Book
from app.modules.loans.models.loan import Loan

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
