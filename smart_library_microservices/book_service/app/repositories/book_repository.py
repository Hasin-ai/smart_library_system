from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, book_data: BookCreate) -> Book:
        """Create a new book"""
        book = Book(**book_data.model_dump())
        book.available_copies = book.copies
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def update(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        """Update book"""
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        update_data = book_data.model_dump(exclude_unset=True)
        
        # Handle copies update
        if 'copies' in update_data:
            new_copies = update_data['copies']
            borrowed_copies = book.copies - book.available_copies
            book.copies = new_copies
            book.available_copies = max(0, new_copies - borrowed_copies)
            del update_data['copies']
        
        # Update other fields
        for field, value in update_data.items():
            setattr(book, field, value)
        
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def update_availability(self, book_id: int, change: int) -> Optional[Book]:
        """Update book availability"""
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        new_available = book.available_copies + change
        if new_available < 0 or new_available > book.copies:
            return None
        
        book.available_copies = new_available
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def set_availability(self, book_id: int, available_copies: int) -> Optional[Book]:
        """Set book availability to specific value"""
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        if available_copies < 0 or available_copies > book.copies:
            return None
        
        book.available_copies = available_copies
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def delete(self, book_id: int) -> bool:
        """Delete book"""
        book = self.get_by_id(book_id)
        if not book:
            return False
        
        self.db.delete(book)
        self.db.commit()
        return True
    
    def search(self, search_term: Optional[str], page: int, per_page: int) -> Tuple[List[Book], int]:
        """Search books with pagination"""
        query = self.db.query(Book)
        
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    Book.title.ilike(search_pattern),
                    Book.author.ilike(search_pattern),
                    Book.isbn.ilike(search_pattern),
                    Book.genre.ilike(search_pattern)
                )
            )
        
        total = query.count()
        books = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return books, total
    
    def count(self) -> int:
        """Count total books"""
        return self.db.query(func.count(Book.id)).scalar()
    
    def get_available_books(self, page: int, per_page: int) -> Tuple[List[Book], int]:
        """Get books with available copies"""
        query = self.db.query(Book).filter(Book.available_copies > 0)
        total = query.count()
        books = query.offset((page - 1) * per_page).limit(per_page).all()
        return books, total
