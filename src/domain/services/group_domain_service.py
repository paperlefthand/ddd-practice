from group import Group
from igroup_repository import IGroupRepository
from injector import inject


class GroupDomainService:
    """グループ周りのドメインサービス. エンティティ(Group)にまたがるビジネスロジックを実装"""

    @inject
    def __init__(self, group_repository: IGroupRepository):
        self.group_repository = group_repository

    def exists(self, group: Group):
        """グループの重複判定
        - 重複判定の詳細なロジックをこのメソッドに記載
        """
        found = self.group_repository.find_by_name(group.name)
        return found is not None
