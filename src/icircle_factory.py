import abc

from circle import Circle, CircleName
from user import User


class ICircleFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, name: CircleName, owner: User) -> Circle:
        raise NotImplementedError
