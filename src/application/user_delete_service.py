from logging import getLogger

from pydantic import BaseModel
from user import UserId
from user_repository import IUserRepository

logger = getLogger(__name__)


class UserDeleteCommand(BaseModel, frozen=True):
    id: str


class UserDeleteService:
    """
    - NOTE 退会処理にはuser_domain_serviceは不要なので登録処理とは別クラスに切り出して凝縮度を高めた
    """

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def handle(self, command: UserDeleteCommand):
        target_id = UserId(value=command.id)
        user = self.user_repository.find_by_id(target_id)
        if not bool(user):
            # NOTE ユーザがもともと存在しなければ"削除成功"とするが,
            # 意図通りでないルートを通って呼ばれた可能性もあるためwarning
            logger.warning("User not found")
        else:
            self.user_repository.delete(user)
            logger.info("User successfully deleted")
