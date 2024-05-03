from domain.models.user.user import UserId
from domain.models.user.user.iuser_repository import IUserRepository
from domain.services.group_domain_service import GroupDomainService
from group import GroupName
from igroup_factory import IGroupFactory
from igroup_repository import IGroupRepository
from injector import inject
from pydantic import BaseModel


class GroupCreateCommand(BaseModel, frozen=True):
    owner_id: str
    name: str


class GroupCreateService:
    # NOTE コンストラクタインジェクションにより依存オブジェクトを注入
    @inject
    def __init__(
        self,
        group_domain_service: GroupDomainService,
        group_repository: IGroupRepository,
        group_factory: IGroupFactory,
        user_repository: IUserRepository,
    ) -> None:
        self.group_domain_service = group_domain_service
        self.group_repository = group_repository
        self.group_factory = group_factory
        self.user_repository = user_repository

    def handle(self, command: GroupCreateCommand):
        # TODO この一連の処理をトランザクション化する(UoW?)
        owner_id = UserId(value=command.owner_id)
        owner = self.user_repository.find_by_id(id=owner_id)
        if owner is None:
            raise Exception("user not found")
        name = GroupName(value=command.name)
        group = self.group_factory.create(name=name, owner=owner)
        if self.group_domain_service.exists(group=group):
            raise Exception("group already exists")
        self.group_repository.save(group=group)
