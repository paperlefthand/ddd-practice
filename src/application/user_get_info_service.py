from logging import getLogger
from typing import Optional

from pydantic import BaseModel
from user import UserId
from user_data import UserData
from user_repository import IUserRepository

logger = getLogger(__name__)


class UserGetInfoCommand(BaseModel, frozen=True):
    id: str


class UserGetInfoService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def handle(self, command: UserGetInfoCommand) -> Optional["UserData"]:
        target_id = UserId(value=command.id)
        user = self.user_repository.find_by_id(target_id)
        return UserData(user) if bool(user) else None
