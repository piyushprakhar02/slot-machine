from app.repositories.user_token_repository import UserTokenRepository
from app.database import Session


class UserTokenService:
    def __init__(self, user_id: str, db: Session):
        self.user_id = user_id
        self.repository = UserTokenRepository(user_id=user_id, db=db)
        self.db = db

    def get_balance(self) -> int:
        balance = self.repository.get_balance()
        return balance

    def credit_balance(self, amount) -> bool:
        current = self.get_balance()
        self.repository.update_balance(current + amount)
        return True

    def debit_balance(self, amount) -> bool:
        current = self.get_balance()
        self.repository.update_balance(current - amount)
        return True
