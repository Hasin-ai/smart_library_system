from typing import List
from sqlalchemy.orm import Session
from app.modules.books.repositories.book_repository import BookRepository
from app.modules.books.models.book import Book
from app.modules.books.schemas.requests import BookCreateRequest, BookUpdateRequest
from app.core.exceptions import BookAlreadyExistsException, BookNotFoundException, BookNotAvailableException

class BookService:
    def __init__(self, db: Session):
        self.repo = BookRepository(db)

    def create_book(self, data: BookCreateRequest) -> Book:
        if self.repo.get_by_isbn(data.isbn):
            raise BookAlreadyExistsException(f"ISBN {data.isbn} exists")
        d = data.model_dump()
        d["available_copies"] = d["copies"]
        return self.repo.create(d)

    def get_book(self, book_id: int) -> Book:
        b = self.repo.get(book_id)
        if not b:
            raise BookNotFoundException(f"Book {book_id} not found")
        return b

    def update_book(self, book_id: int, data: BookUpdateRequest) -> Book:
        b = self.get_book(book_id)
        dd = data.model_dump(exclude_unset=True)
        if "isbn" in dd and dd["isbn"] != b.isbn and self.repo.get_by_isbn(dd["isbn"]):
            raise BookAlreadyExistsException(f"ISBN {dd['isbn']} exists")
        if "copies" in dd:
            borrowed = b.copies - b.available_copies
            dd["available_copies"] = max(0, dd["copies"] - borrowed)
        return self.repo.update(book_id, dd)

    def delete_book(self, book_id: int) -> bool:
        b = self.get_book(book_id)
        if b.copies != b.available_copies:
            raise BookNotAvailableException("Active loans exist")
        return self.repo.delete(book_id)

    def list_books(self, term: str, skip: int, limit: int) -> List[Book]:
        return self.repo.search(term, skip, limit)

    def reserve_book(self, book_id: int) -> Book:
        book = self.get_book(book_id)
        if book.available_copies < 1:
            raise BookNotAvailableException("No copies available")
        return self.repo.update(book_id, {"available_copies": book.available_copies - 1})

    def return_book(self, book_id: int) -> Book:
        book = self.get_book(book_id)
        return self.repo.update(book_id, {"available_copies": book.available_copies + 1})
