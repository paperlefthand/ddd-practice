from user import User
from user_repository import IUserRepository


class UserService:
    """ユーザ周りのドメインサービス. エンティティにまたがるビジネスロジックを実装"""

    def __init__(self, user_repository: "IUserRepository") -> None:
        self.user_repository: IUserRepository = user_repository

    def exists(self, user: "User") -> bool:
        """指定したユーザが存在するか判定(重複判定?)"""
        found = self.user_repository.find_by_id(user.id)
        return found is not None
