from typing import List, Tuple
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.core.logging import logger

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        logger.info(f"Creating user with email: {user_data.email}")
        
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            logger.warning(f"User with email {user_data.email} already exists")
            raise UserAlreadyExistsException(user_data.email)
        
        # Create user
        user = self.repository.create(user_data)
        logger.info(f"User created with id: {user.id}")
        
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID"""
        logger.info(f"Fetching user with id: {user_id}")
        
        user = self.repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User with id {user_id} not found")
            raise UserNotFoundException(user_id)
        
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user"""
        logger.info(f"Updating user with id: {user_id}")
        
        # Check if user exists
        user = self.repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User with id {user_id} not found")
            raise UserNotFoundException(user_id)
        
        # Check if email is being updated and already exists
        if user_data.email and user_data.email != user.email:
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user:
                logger.warning(f"User with email {user_data.email} already exists")
                raise UserAlreadyExistsException(user_data.email)
        
        # Update user
        updated_user = self.repository.update(user_id, user_data)
        logger.info(f"User {user_id} updated successfully")
        
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        logger.info(f"Deleting user with id: {user_id}")
        
        if not self.repository.get_by_id(user_id):
            logger.warning(f"User with id {user_id} not found")
            raise UserNotFoundException(user_id)
        
        result = self.repository.delete(user_id)
        logger.info(f"User {user_id} deleted successfully")
        
        return result
    
    def list_users(self, page: int, per_page: int) -> Tuple[List[UserResponse], int]:
        """List all users with pagination"""
        logger.info(f"Listing users - page: {page}, per_page: {per_page}")
        
        users, total = self.repository.list_all(page, per_page)
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        return user_responses, total
