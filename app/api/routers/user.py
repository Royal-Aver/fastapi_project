from fastapi import Depends, APIRouter
from fastapi import HTTPException
from app.core.db import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.exceptions.user import UserNotFoundError, UserAlreadyExistsError


router = APIRouter()


@router.get("/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        user = service.get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        email=user.email,
        is_banned=user.is_banned
    )



@router.post("/users")
def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        new_user = service.create_user(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail="User already exists")

    return UserResponse.model_validate(new_user)


@router.patch("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db=Depends(get_db)):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    try:
        updated_user = service.update_user(user_id, data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=409, detail="User not found")

    return UserResponse.model_validate(updated_user)