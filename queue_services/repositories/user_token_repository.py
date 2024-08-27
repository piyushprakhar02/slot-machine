from model import Token


class UserTokenRepository:
    def __init__(self, user_id: str, db):
        self.user_id = user_id
        self.db = db

    def get_balance(self) -> int:
        """Fetch the token balance for the user."""
        token = self.db.query(Token).filter(Token.user_id == self.user_id).first()
        return token.balance if token else 0

    def update_balance(self, new_balance: int):
        """Update the token balance for the user or create a new entry if it doesn't exist."""
        token = self.db.query(Token).filter(Token.user_id == self.user_id).first()

        if token:
            token.balance = new_balance
        else:
            token = Token(user_id=self.user_id, balance=new_balance)
            self.db.add(token)

        self.db.commit()
