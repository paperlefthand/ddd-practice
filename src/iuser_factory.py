import abc

from mail_address import MailAddress
from user import User, UserName


class IUserFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, name: UserName, email: MailAddress) -> User:
        raise NotImplementedError
