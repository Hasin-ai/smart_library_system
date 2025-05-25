from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository
from app.schemas.book import (
    BookCreate, BookUpdate, BookResponse, 
    BookAvailabilityUpdate, AvailabilityOperation
)
from app.core.exceptions import (
    BookNotFoundException, BookAlreadyExistsException,
    InsufficientCopiesException, BookNotDeletableException
)
from app.core.logging import logger

class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)
    
    def create_book(self, book_data: BookCreate) -> BookResponse:
        """Create a new book"""
        logger.info(f"Creating book with ISBN: {book_data.isbn}")
        
        # Check if book already exists
        existing_book = self.repository.get_by_isbn(book_data.isbn)
        if existing_book:
            logger.warning(f"Book with ISBN {book_data.isbn} already exists")
            raise BookAlreadyExistsException(book_data.isbn)
        
        # Create book
        book = self.repository.create(book_data)
        logger.info(f"Book created with id: {book.id}")
        
        return BookResponse.model_validate(book)
    
    def get_book(self, book_id: int) -> BookResponse:
        """Get book by ID"""
        logger.info(f"Fetching book with id: {book_id}")
        
        book = self.repository.get_by_id(book_id)
        if not book:
            logger.warning(f"Book with id {book_id} not found")
            raise BookNotFoundException(book_id)
        
        return BookResponse.model_validate(book)
    
    def update_book(self, book_id: int, book_data: BookUpdate) -> BookResponse:
        """Update book"""
        logger.info(f"Updating book with id: {book_id}")
        
        # Check if book exists
        book = self.repository.get_by_id(book_id)
        if not book:
            logger.warning(f"Book with id {book_id} not found")
            raise BookNotFoundException(book_id)
        
        # Check if ISBN is being updated and already exists
        if book_data.isbn and book_data.isbn != book.isbn:
            existing_book = self.repository.get_by_isbn(book_data.isbn)
            if existing_book:
                logger.warning(f"Book with ISBN {book_data.isbn} already exists")
                raise BookAlreadyExistsException(book_data.isbn)
        
        # Update book
        updated_book = self.repository.update(book_id, book_data)
        logger.info(f"Book {book_id} updated successfully")
        
        return BookResponse.model_validate(updated_book)
    
    def update_availability(self, book_id: int, update: BookAvailabilityUpdate) -> dict:
        """Update book availability"""
        logger.info(f"Updating availability for book {book_id}")
        
        book = self.repository.get_by_id(book_id)
        if not book:
            logger.warning(f"Book with id {book_id} not found")
            raise BookNotFoundException(book_id)
        
        # Handle operation-based update
        if update.operation:
            if update.operation == AvailabilityOperation.INCREMENT:
                result = self.repository.update_availability(book_id, 1)
            else:  # DECREMENT
                if book.available_copies < 1:
                    raise InsufficientCopiesException(book_id, 1, book.available_copies)
                result = self.repository.update_availability(book_id, -1)
        
        # Handle explicit availability update
        elif update.available_copies is not None:
            if update.available_copies > book.copies:
                raise InsufficientCopiesException(
                    book_id, 
                    update.available_copies, 
                    book.copies
                )
            result = self.repository.set_availability(book_id, update.available_copies)
        else:
            # No operation specified
            result = book
        
        logger.info(f"Book {book_id} availability updated to {result.available_copies}")
        
        return {
            "id": result.id,
            "available_copies": result.available_copies,
            "updated_at": result.updated_at
        }
    
    def delete_book(self, book_id: int) -> bool:
        """Delete book"""
        logger.info(f"Deleting book with id: {book_id}")
        
        book = self.repository.get_by_id(book_id)
        if not book:
            logger.warning(f"Book with id {book_id} not found")
            raise BookNotFoundException(book_id)
        
        # Check if book can be deleted
        if book.available_copies < book.copies:
            borrowed = book.copies - book.available_copies
            logger.warning(f"Book {book_id} has {borrowed} borrowed copies")
            raise BookNotDeletableException(
                book_id, 
                f"{borrowed} copies are currently borrowed"
            )
        
        result = self.repository.delete(book_id)
        logger.info(f"Book {book_id} deleted successfully")
        
        return result
    
    def search_books(
        self, 
        search_term: Optional[str], 
        page: int, 
        per_page: int
    ) -> Tuple[List[BookResponse], int]:
        """Search books with pagination"""
        logger.info(f"Searching books - term: {search_term}, page: {page}, per_page: {per_page}")
        
        books, total = self.repository.search(search_term, page, per_page)
        book_responses = [BookResponse.model_validate(book) for book in books]
        
        return book_responses, total
    
    def get_available_books(self, page: int, per_page: int) -> Tuple[List[BookResponse], int]:
        """Get books with available copies"""
        logger.info(f"Fetching available books - page: {page}, per_page: {per_page}")
        
        books, total = self.repository.get_available_books(page, per_page)
        book_responses = [BookResponse.model_validate(book) for book in books]
        
        return book_responses, total
