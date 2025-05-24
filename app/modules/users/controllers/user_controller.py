from typing import List
from sqlalchemy.orm import Session
from app.modules.users.services.user_service import UserService
from app.modules.users.schemas.requests import UserCreateRequest, UserUpdateRequest
from app.modules.users.schemas.responses import UserResponse

class UserController:
    def __init__(self, db: Session):
        self.svc = UserService(db)

    def create(self, data: UserCreateRequest) -> UserResponse:
        u = self.svc.create_user(data)
        return UserResponse.model_validate(u)

    def get(self, user_id: int) -> UserResponse:
        u = self.svc.get_user(user_id)
        return UserResponse.model_validate(u)

    def update(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        u = self.svc.update_user(user_id, data)
        return UserResponse.model_validate(u)

    def list(self, skip: int, limit: int) -> List[UserResponse]:
        users = self.svc.get_all_users(skip, limit)
        return [UserResponse.model_validate(u) for u in users]
