import uuid

from pydantic import BaseModel, Field


class UserId(BaseModel, frozen=True):
    value: str = Field(min_length=3, max_length=32)


class UserName(BaseModel, frozen=True):
    value: str = Field(min_length=3, max_length=32)


class User:
    # HACK: コンストラクタの引数名とgetter/setterのプロパティ名が異なると嫌なのでPydanticにしていない.
    # NOTE: ユーザIDの指定がなければUUIDで自動採番
    # HACK: ユーザIDの仕様で決められた制限文字数が32文字未満の場合どうするか
    def __init__(
        self,
        name: UserName,
        id: UserId = UserId(value=str(uuid.uuid4()).replace("-", "")),
    ):
        if not isinstance(name, UserName):
            raise TypeError("name is not an instance of UserName")
        if not isinstance(id, UserId):
            raise TypeError("id is not an instance of UserId")
        self._id: UserId = id
        self._name: UserName = name

    # NOTE: getterのみ定義することでユーザIDをimmutableにしている
    @property
    def id(self) -> UserId:
        return self._id

    @property
    def name(self) -> UserName:
        return self._name

    # NOTE: ユーザ名は後から変更可能にしている
    @name.setter
    def name(self, name: "UserName"):
        if not isinstance(name, UserName):
            raise TypeError("name is not an instance of UserName")
        self._name = name

    def equals(self, user: "User"):
        if not isinstance(user, User):
            raise TypeError("user is not an instance of User")
        return self._id.value == user.id.value
