from circle import CircleName
from circle_domain_service import CircleDomainService
from icircle_factory import ICircleFactory
from icircle_repository import ICircleRepository
from iuser_repository import IUserRepository
from pydantic import BaseModel
from user import UserId


class CircleCreateCommand(BaseModel):
    id: str
    name: str


class CircleApplicationService:
    def __init__(
        self,
        circle_domain_service: CircleDomainService,
        circle_repository: ICircleRepository,
        circle_factory: ICircleFactory,
        user_repository: IUserRepository,
    ) -> None:
        self.circle_domain_service = circle_domain_service
        self.circle_repository = circle_repository
        self.circle_factory = circle_factory
        self.user_repository = user_repository

    def create(self, command: CircleCreateCommand):
        # TODO この一連の処理をトランザクション化する(UoW?)
        owner_id = UserId(value=command.id)
        owner = self.user_repository.find_by_id(id=owner_id)
        if owner is None:
            raise Exception("user not found")
        name = CircleName(value=command.name)
        circle = self.circle_factory.create(name=name, owner=owner)
        if self.circle_domain_service.exists(circle=circle):
            raise Exception("circle already exists")
        self.circle_repository.save(circle=circle)
