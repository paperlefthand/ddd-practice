import copy
from typing import Optional

from application.user.mail_address import MailAddress
from domain.models.user.iuser_repository import IUserRepository
from domain.models.user.user import User, UserId, UserName


class UserMockRepository(IUserRepository):
    def __init__(self):
        self.db: dict[str, User] = {}

    def save(self, user: User):
        id = user.id.value
        self.db[id] = copy.deepcopy(user)

    def delete(self, user: User):
        id = user.id.value
        del self.db[id]

    def find_by_id(self, id: UserId) -> Optional["User"]:
        return self.db[id.value]

    def find_by_email(self, email: MailAddress) -> Optional["User"]:
        for user in self.db.values():
            if user.email.value == email.value:
                return user

    def find_by_name(self, name: UserName) -> list[User]:
        return [user for user in self.db.values() if user.name.value == name.value]
