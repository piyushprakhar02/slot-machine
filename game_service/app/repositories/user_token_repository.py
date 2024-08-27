from sqlalchemy.orm import Session
from app.models import Token


class UserTokenRepository:
    def __init__(self, user_id: str, db: Session):
        self.user_id = user_id
        self.db = db

    def get_balance(self) -> int:
        """Fetch the token balance for the user."""
        token = self.db.query(Token).filter(Token.user_id == self.user_id).first()
        return token.balance if token else 0

    def update_balance(self, new_balance: int):
        """Update the token balance for the user."""
        self.db.query(Token).filter(Token.user_id == self.user_id).update({Token.balance: new_balance})
        self.db.commit()
