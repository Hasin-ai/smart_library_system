from typing import List
from sqlalchemy.orm import Session
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.models.user import User
from app.modules.users.schemas.requests import UserCreateRequest, UserUpdateRequest
from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreateRequest) -> User:
        if self.repo.get_by_email(data.email):
            raise UserAlreadyExistsException(f"Email {data.email} already exists")
        return self.repo.create(data.model_dump())

    def get_user(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        return user

    def update_user(self, user_id: int, data: UserUpdateRequest) -> User:
        user = self.get_user(user_id)
        if data.email and data.email != user.email and self.repo.get_by_email(data.email):
            raise UserAlreadyExistsException(f"Email {data.email} already exists")
        return self.repo.update(user_id, data.model_dump(exclude_unset=True))

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repo.get_all(skip, limit)
