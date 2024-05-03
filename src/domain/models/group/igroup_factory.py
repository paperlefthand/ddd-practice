import abc

from domain.models.user.user import User
from group import Group, GroupName


class IGroupFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, name: GroupName, owner: User) -> Group:
        raise NotImplementedError
