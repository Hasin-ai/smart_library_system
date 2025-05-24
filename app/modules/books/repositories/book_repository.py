from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.shared.base_repository import BaseRepository
from app.modules.books.models.book import Book

class BookRepository(BaseRepository[Book]):
    def __init__(self, db: Session):
        super().__init__(Book, db)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def search(self, term: str, skip: int, limit: int) -> List[Book]:
        q = self.db.query(Book)
        if term:
            q = q.filter(or_(
                Book.title.ilike(f"%{term}%"),
                Book.author.ilike(f"%{term}%"),
                Book.genre.ilike(f"%{term}%"),
            ))
        return q.offset(skip).limit(limit).all()
