from domain.models.user.iuser_repository import IUserRepository
from group import Group
from injector import inject


class GroupFullSpecification:
    """グループの定員上限の仕様クラス"""

    # NOTE: 判定に当たって,リポジトリへの問い合わせが必要となった場合,
    # Groupエンティティにリポジトリを操作させるべきでない.

    # NOTE コンストラクタインジェクションにより依存オブジェクトを注入
    @inject
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def is_satisfied_by(self, group: Group):
        # OPTIMIZE クエリし過ぎ
        premium_user_num = 0
        for id in group.members:
            user = self.user_repository.find_by_id(id)
            if user is not None and user.is_premium():
                premium_user_num += 1
        user_count_limit = 30 if premium_user_num < 10 else 50
        return group.count_members() >= user_count_limit
