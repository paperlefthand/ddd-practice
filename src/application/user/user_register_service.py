from application.user.mail_address import MailAddress
from domain.models.user.iuser_factory import IUserFactory
from domain.models.user.iuser_repository import IUserRepository
from domain.models.user.user import UserName
from domain.services.user_domain_service import UserDomainService
from injector import inject
from pydantic import BaseModel


class UserRegisterCommand(BaseModel, frozen=True):
    name: str
    email: str


class UserRegisterService:
    """ユーザの登録ユースケースを実現するアプリケーションサービス"""

    # NOTE コンストラクタインジェクションにより依存オブジェクトを注入
    @inject
    def __init__(
        self,
        user_repository: IUserRepository,
        user_domain_service: UserDomainService,
        user_factory: IUserFactory,
    ) -> None:
        self.user_repository = user_repository
        self.user_domain_service = user_domain_service
        self.user_factory = user_factory

    def handle(self, command: UserRegisterCommand) -> None:
        user = self.user_factory.create(
            email=MailAddress(value=command.email), name=UserName(value=command.name)
        )
        if self.user_domain_service.exists(user):
            # HACK 重複の詳細はここではわからないので例外メッセージに発生原因を出力できないがそれでよいか.
            raise Exception("User already exists")
        self.user_repository.save(user=user)
