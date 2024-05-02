from logging import getLogger
from typing import Optional

from mail_address import MailAddress
from pydantic import BaseModel
from user import UserId, UserName
from user_domain_service import UserDomainService
from user_repository import IUserRepository

logger = getLogger(__name__)


class UserUpdateCommand(BaseModel, frozen=True):
    """ファサードの役割"""

    id: str
    name: Optional[str] = None
    email: Optional[str] = None


class UserUpdateInfoService:
    """ユーザ周りのアプリケーションサービス.ドメインオブジェクトのふるまいを呼び出す.
    - ドメインオブジェクトは直接公開せず,アプリケーションサービスを介して触らせる.
    - ドメインのルールはアプリケーションサービスではなくドメインオブジェクトに記述する.
      例: ドメインサービスのexistsを呼び出す(具体的な重複判定内容には踏み込まない)
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        user_domain_service: UserDomainService,
    ) -> None:
        self.user_repository: IUserRepository = user_repository
        self.user_domain_service: UserDomainService = user_domain_service

    def handle(self, command: UserUpdateCommand) -> None:
        target_id = UserId(value=command.id)
        user = self.user_repository.find_by_id(target_id)
        if not bool(user):
            raise Exception("User not found")

        name = command.name
        if bool(name):
            user.name = UserName(value=name)

        email = command.email
        if bool(email):
            user.email = MailAddress(value=email)

        # NOTE 具体的な重複判定ロジックについては知らない
        if self.user_domain_service.exists(user):
            raise Exception("既存ユーザのデータと重複しています")

        self.user_repository.save(user)
        logger.info("User successfully updated")
