from injector import inject
from iuser_repository import IUserRepository
from user import User


class UserDomainService:
    """ユーザ周りのドメインサービス. エンティティ(User)にまたがるビジネスロジックを実装"""

    @inject
    def __init__(self, user_repository: "IUserRepository") -> None:
        self.user_repository: IUserRepository = user_repository

    def exists(self, user: "User") -> bool:
        """ユーザの重複判定
        - 重複判定ロジックを変更するにはここだけ変更すれば良い
        """
        found = self.user_repository.find_by_email(user.email)
        return found is not None
