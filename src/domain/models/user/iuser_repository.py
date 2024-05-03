import abc
from typing import Optional

from application.user.mail_address import MailAddress
from domain.models.user.user import User, UserId, UserName


class IUserRepository(metaclass=abc.ABCMeta):
    """ユーザリポジトリのインターフェース"""

    # リポジトリはユーザオブジェクトのライフサイクル(永続化,再構築,削除)の責務を負う
    # 実際のデータベース操作の詳細をサービスクラスから隠ぺいする. メソッド名は業務の関心事.

    @abc.abstractmethod
    def save(self, user: "User"):
        raise NotImplementedError(self.save)

    @abc.abstractmethod
    def find_by_id(self, id: "UserId") -> Optional["User"]:
        raise NotImplementedError(self.find_by_id)

    @abc.abstractmethod
    def find_by_email(self, email: "MailAddress") -> Optional["User"]:
        raise NotImplementedError(self.find_by_email)

    @abc.abstractmethod
    def find_by_name(self, name: "UserName") -> list["User"]:
        raise NotImplementedError(self.find_by_name)

    @abc.abstractmethod
    def delete(self, user: "User"):
        raise NotImplementedError(self.save)
