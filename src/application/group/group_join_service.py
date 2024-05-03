from domain.models.group.group_full_specification import GroupFullSpecification
from domain.models.user.user import UserId
from domain.models.user.user.iuser_repository import IUserRepository
from domain.services.group_domain_service import GroupDomainService
from group import GroupFullException, GroupId
from igroup_factory import IGroupFactory
from igroup_repository import IGroupRepository
from injector import inject
from pydantic import BaseModel


class GroupJoinCommand(BaseModel, frozen=True):
    user_id: str
    group_id: str


class GroupJoinService:
    @inject
    def __init__(
        self,
        group_repository: IGroupRepository,
        user_repository: IUserRepository,
        group_factory: IGroupFactory,
        group_domain_service: GroupDomainService,
    ):
        self.group_repository = group_repository
        self.user_repository = user_repository
        self.group_factory = group_factory
        self.group_domain_service = group_domain_service

    def handle(self, command: GroupJoinCommand):
        group_id = GroupId(value=command.group_id)
        group = self.group_repository.find_by_id(group_id)
        if group is None:
            raise Exception("group not found")
        group_full_specification = GroupFullSpecification(self.user_repository)
        if group_full_specification.is_satisfied_by(group):
            raise GroupFullException(group_id=group_id)
        user_id = UserId(value=command.user_id)
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise Exception("user not found")
        group.join(user)
        self.group_repository.save(group)
