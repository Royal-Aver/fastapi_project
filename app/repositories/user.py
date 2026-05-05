from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def save_user(self, user: User):
        self.session.add(user)