#!/usr/bin/env python3
"""Seed sample data"""
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all models first to ensure they're registered with SQLAlchemy
from app.modules.users.models.user import User, UserRole
from app.modules.books.models.book import Book
from app.modules.loans.models.loan import Loan  # Import Loan model to register relationships

from sqlalchemy.orm import Session
from app.config.database import SessionLocal

def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Data already seeded!")
            return
            
        # Create sample users
        users = [
            User(name="John Doe", email="john@example.com", role=UserRole.STUDENT),
            User(name="Jane Smith", email="jane@example.com", role=UserRole.FACULTY),
            User(name="Admin User", email="admin@example.com", role=UserRole.ADMIN),
        ]
        
        for user in users:
            db.add(user)
            
        # Create sample books
        books = [
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="978-0-7432-7356-5", genre="Fiction", copies=3, available_copies=3),
            Book(title="To Kill a Mockingbird", author="Harper Lee", isbn="978-0-06-112008-4", genre="Fiction", copies=2, available_copies=2),
            Book(title="1984", author="George Orwell", isbn="978-0-452-28423-4", genre="Dystopian", copies=4, available_copies=4),
            Book(title="Pride and Prejudice", author="Jane Austen", isbn="978-0-14-143951-8", genre="Romance", copies=2, available_copies=2),
        ]
        
        for book in books:
            db.add(book)
            
        db.commit()
        print("Sample data seeded successfully!")
        print(f"✅ Created {len(users)} users")
        print(f"✅ Created {len(books)} books")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()