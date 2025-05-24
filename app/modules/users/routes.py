from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.users.controllers.user_controller import UserController
from app.modules.users.schemas.requests import UserCreateRequest, UserUpdateRequest
from app.modules.users.schemas.responses import UserResponse
from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreateRequest, db: Session = Depends(get_db)):
    ctrl = UserController(db)
    try:
        return ctrl.create(data)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    ctrl = UserController(db)
    try:
        return ctrl.get(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdateRequest, db: Session = Depends(get_db)):
    ctrl = UserController(db)
    try:
        return ctrl.update(user_id, data)
    except (UserNotFoundException, UserAlreadyExistsException) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return UserController(db).list(skip, limit)
