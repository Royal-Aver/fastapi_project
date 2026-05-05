from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.models.user import User
from app.exceptions.user import UserNotFoundError, UserAlreadyExistsError


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user

    def create_user(self, user: UserCreate) -> User:
        existing_user = self.user_repo.get_user_by_email(user.email)

        if existing_user:
            raise UserAlreadyExistsError()

        hashed_password = "hashed" + user.password

        new_user = User(email=user.email, password_hash=hashed_password)
        self.user_repo.save_user(new_user)

        return user

    def update_user(self, user_id: int, data: UserUpdate):
        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundError()

        if data.email is not None:
            user.email = data.email

        if data.password is not None:
            user.password_hash = "hashed" + data.password

        return user