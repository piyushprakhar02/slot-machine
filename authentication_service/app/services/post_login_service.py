from decouple import config

from app.services.sns_service import SnsService
from constant import Constant


class PostLoginService:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def perform_taks(self) -> None:
        message = {
            "transaction_type": Constant.CREDIT_TOKEN,
            "transaction_amount": Constant.NUMBER_OF_TOKENS_ON_LOGIN,
            "user_id": self.user_id
        }

        sns_service = SnsService()
        sns_service.publish(message_body=message)
        return
