from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.books.controllers.book_controller import BookController
from app.modules.books.schemas.requests import BookCreateRequest, BookUpdateRequest
from app.modules.books.schemas.responses import BookResponse
from app.core.exceptions import BookAlreadyExistsException, BookNotFoundException, BookNotAvailableException

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(data: BookCreateRequest, db: Session = Depends(get_db)):
    ctrl = BookController(db)
    try:
        return ctrl.create(data)
    except BookAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    ctrl = BookController(db)
    try:
        return ctrl.get(book_id)
    except BookNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, data: BookUpdateRequest, db: Session = Depends(get_db)):
    ctrl = BookController(db)
    try:
        return ctrl.update(book_id, data)
    except (BookNotFoundException, BookAlreadyExistsException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    ctrl = BookController(db)
    try:
        ctrl.delete(book_id)
    except (BookNotFoundException, BookNotAvailableException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BookResponse])
async def list_books(
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return BookController(db).list(search or "", skip, limit)
