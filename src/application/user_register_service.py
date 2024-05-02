from logging import getLogger

from injector import inject
from iuser_factory import IUserFactory
from mail_address import MailAddress
from pydantic import BaseModel
from user import UserName
from user_domain_service import UserDomainService
from user_repository import IUserRepository

logger = getLogger(__name__)


class UserRegisterCommand(BaseModel, frozen=True):
    name: str
    email: str


class UserRegisterService:
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
            raise Exception("User already exists")
        self.user_repository.save(user)
