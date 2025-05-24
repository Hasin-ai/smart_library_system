from typing import List
from sqlalchemy.orm import Session
from app.modules.books.services.book_service import BookService
from app.modules.books.schemas.requests import BookCreateRequest, BookUpdateRequest
from app.modules.books.schemas.responses import BookResponse

class BookController:
    def __init__(self, db: Session):
        self.svc = BookService(db)

    def create(self, data: BookCreateRequest) -> BookResponse:
        b = self.svc.create_book(data)
        return BookResponse.model_validate(b)

    def get(self, book_id: int) -> BookResponse:
        b = self.svc.get_book(book_id)
        return BookResponse.model_validate(b)

    def update(self, book_id: int, data: BookUpdateRequest) -> BookResponse:
        b = self.svc.update_book(book_id, data)
        return BookResponse.model_validate(b)

    def delete(self, book_id: int):
        self.svc.delete_book(book_id)

    def list(self, term: str, skip: int, limit: int) -> List[BookResponse]:
        books = self.svc.list_books(term, skip, limit)
        return [BookResponse.model_validate(b) for b in books]
