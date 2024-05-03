from logging import getLogger
from typing import Optional

from application.user.mail_address import MailAddress
from domain.models.user.iuser_repository import IUserRepository
from domain.models.user.user import UserId, UserName
from domain.services.user_domain_service import UserDomainService
from pydantic import BaseModel

logger = getLogger(__name__)


class UserUpdateCommand(BaseModel, frozen=True):
    """ファサードの役割"""

    id: str
    name: Optional[str] = None
    email: Optional[str] = None


class UserUpdateInfoService:
    """ユーザ更新ユースケースを実現するアプリケーションサービス.ドメインオブジェクトのふるまいを呼び出す.
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
        # HACK handleをトランザクション化したい
        target_id = UserId(value=command.id)
        user = self.user_repository.find_by_id(target_id)
        if not bool(user):
            raise Exception("User not found")

        name = command.name
        if bool(name):
            user.change_name(UserName(value=name))

        email = command.email
        if bool(email):
            user.change_email(MailAddress(value=email))

        # NOTE 具体的な重複判定ロジックについては知らない
        if self.user_domain_service.exists(user):
            raise Exception("既存ユーザのデータと重複しています")

        self.user_repository.save(user)
        logger.info("User successfully updated")
