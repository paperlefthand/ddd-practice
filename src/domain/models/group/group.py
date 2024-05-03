from domain.models.user.user import User, UserId
from pydantic import BaseModel, Field, PrivateAttr


class GroupId(BaseModel):
    value: str = Field(min_length=3, max_length=32)


class GroupName(BaseModel):
    value: str = Field(min_length=3, max_length=20)

    def equals(self, other):
        return self.value == other.value


class GroupFullException(Exception):
    def __init__(self, group_id: GroupId):
        self.group_id = group_id


class Group(BaseModel):
    id: GroupId = Field(frozen=True)
    _name: GroupName = PrivateAttr()
    _owner: User = PrivateAttr()
    _members: list[UserId] = PrivateAttr()

    def __init__(
        self, id: GroupId, name: GroupName, owner: User, members: list[UserId]
    ):
        assert isinstance(id, GroupId)
        assert isinstance(name, GroupName)
        assert isinstance(owner, User)
        assert isinstance(members, list)
        super().__init__(id=id)
        self._name: GroupName = name
        self._owner: User = owner
        self._members: list[UserId] = members

    @property
    def name(self) -> GroupName:
        return self._name

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def members(self) -> list[UserId]:
        return self._members

    def count_members(self) -> int:
        # "オーナーを含めたメンバー数"という仕様を反映
        return len(self._members) + 1

    def is_full(self):
        """グループが定員上限に達しているか"""
        # NOTE: 参加可否の判定ロジックがエンティティ内部で判定できるならここにとどめる.
        # 判定が複雑なのでGroupFullSpecificationで行っている.
        # return self.count_members() >= 30
        pass

    def join(self, user: User):
        """グループへの参加"""
        # NOTE: グループメンバーに対する操作はGroupクラスに集約.
        # 外部からは直接memberには触らせずgroup.join(user)という形式で実行させる.
        # if self.is_full():
        #     raise GroupFullException(self.id)
        if user.id in self._members:
            return
        if user.id == self._owner.id:
            return
        self._members.append(user.id)
