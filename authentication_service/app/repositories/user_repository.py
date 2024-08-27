from app.database import Session
from sqlalchemy import Date
from sqlalchemy.exc import IntegrityError

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, id: str, email: str, name: str, birthdate: Date) -> User:
        """Add a new user to the database."""
        new_user = User(id=id, email=email, name=name, birthdate=birthdate)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user

        except IntegrityError:
            self.db.rollback()
            raise ValueError("User with this email already exists")

    def get_user(self, email: str) -> User:
        """Retrieve a user by email"""

        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("User not found")
        return user

    def update_user(self, email: str, data: dict) -> User:
        """Update user information"""

        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("User not found")

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Failed to update user")
