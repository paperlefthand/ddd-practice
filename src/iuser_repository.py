import abc
from typing import Optional

from user import User, UserId, UserName


class IUserRepository(metaclass=abc.ABCMeta):
    """ユーザリポジトリのインターフェース
    リポジトリはユーザオブジェクトの永続化の責務を負う
    """

    @abc.abstractmethod
    def save(self, user: "User"):
        raise NotImplementedError(self.save)

    @abc.abstractmethod
    def find_by_id(self, id: "UserId") -> Optional["User"]:
        raise NotImplementedError(self.find_by_id)

    @abc.abstractmethod
    def find_by_name(self, name: "UserName") -> list["User"]:
        raise NotImplementedError(self.find_by_name)
