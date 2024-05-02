import abc
from typing import Optional

from circle import Circle, CircleId, CircleName


class ICircleRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, circle: Circle):
        raise NotImplementedError(self.save)

    @abc.abstractmethod
    def find_by_id(self, id: CircleId) -> Optional[Circle]:
        raise NotImplementedError(self.find_by_id)

    @abc.abstractmethod
    def find_by_name(self, name: CircleName) -> Optional[Circle]:
        raise NotImplementedError(self.find_by_name)
