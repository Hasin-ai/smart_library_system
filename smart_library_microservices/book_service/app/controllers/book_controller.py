from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.config.database import get_db
from app.services.book_service import BookService
from app.schemas.book import (
    BookCreate, BookUpdate, BookResponse, BookSearchResponse,
    BookAvailabilityUpdate, BookAvailabilityResponse
)
from app.core.exceptions import BookServiceException
from app.core.logging import logger

router = APIRouter(prefix="/api/books", tags=["books"])

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
) -> BookResponse:
    """Create a new book"""
    try:
        service = BookService(db)
        return service.create_book(book_data)
    except BookServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error creating book: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> BookResponse:
    """Get book by ID"""
    try:
        service = BookService(db)
        return service.get_book(book_id)
    except BookServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error fetching book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
) -> BookResponse:
    """Update book"""
    try:
        service = BookService(db)
        return service.update_book(book_id, book_data)
    except BookServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error updating book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/{book_id}/availability", response_model=BookAvailabilityResponse)
async def update_book_availability(
    book_id: int,
    update: BookAvailabilityUpdate,
    db: Session = Depends(get_db)
) -> BookAvailabilityResponse:
    """Update book availability"""
    try:
        service = BookService(db)
        result = service.update_availability(book_id, update)
        return BookAvailabilityResponse(**result)
    except BookServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error updating book {book_id} availability: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> None:
    """Delete book"""
    try:
        service = BookService(db)
        service.delete_book(book_id)
    except BookServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error deleting book {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("", response_model=BookSearchResponse)
async def search_books(
    search: Optional[str] = Query(None, description="Search term"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> BookSearchResponse:
    """Search books with pagination"""
    try:
        service = BookService(db)
        books, total = service.search_books(search, page, per_page)
        
        return BookSearchResponse(
            books=books,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        logger.error(f"Unexpected error searching books: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
