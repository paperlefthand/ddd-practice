import abc
from typing import Optional

from group import Group, GroupId, GroupName


class IGroupRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, group: Group):
        raise NotImplementedError(self.save)

    @abc.abstractmethod
    def find_by_id(self, id: GroupId) -> Optional[Group]:
        raise NotImplementedError(self.find_by_id)

    @abc.abstractmethod
    def find_by_name(self, name: GroupName) -> Optional[Group]:
        raise NotImplementedError(self.find_by_name)
