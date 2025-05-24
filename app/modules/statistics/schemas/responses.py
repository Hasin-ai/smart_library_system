from pydantic import BaseModel

class PopularBookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    borrow_count: int

class ActiveUserResponse(BaseModel):
    user_id: int
    name: str
    total_borrows: int
    current_borrows: int

class SystemOverviewResponse(BaseModel):
    total_books: int
    total_users: int
    active_loans: int
    overdue_loans: int
    available_books: int
    total_loans_issued: int
