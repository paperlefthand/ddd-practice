import abc

from application.user.mail_address import MailAddress
from domain.models.user.user import User, UserName


class IUserFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, name: UserName, email: MailAddress) -> User:
        raise NotImplementedError
