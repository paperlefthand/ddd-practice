from mail_address import MailAddress
from pydantic import BaseModel, Field


class UserId(BaseModel, frozen=True):
    """ユーザIDの値オブジェクト(immutable)
    - NOTE フィールドの制約は仕様書から決定する
    """

    value: str = Field(min_length=3, max_length=32)


class UserName(BaseModel, frozen=True):
    """ユーザ名の値オブジェクト(immutable)
    - NOTE フィールドの制約は仕様書から決定する
    """

    value: str = Field(min_length=3, max_length=20)


class User:
    """ユーザエンティティ
    - HACK: コンストラクタの引数名とgetter/setterのプロパティ名が異なると嫌なのでPydanticにしていない.
    """

    def __init__(
        self,
        id: UserId,
        name: UserName,
        email: MailAddress,
    ):
        # NOTE 型検査.これに引っかかるということはプログラムミスの可能性が高い.
        assert isinstance(id, UserId)
        assert isinstance(name, UserName)
        assert isinstance(email, MailAddress)
        self._id: UserId = id
        self._name: UserName = name
        self._email: MailAddress = email

    # NOTE: getterのみ定義することでユーザIDをimmutableにしている
    @property
    def id(self) -> UserId:
        return self._id

    @property
    def name(self) -> UserName:
        return self._name

    # NOTE: ユーザ名は後から変更可能(mutable)にしている
    @name.setter
    def name(self, name: "UserName"):
        if not isinstance(name, UserName):
            raise TypeError("name is not an instance of UserName")
        self._name = name

    @property
    def email(self) -> MailAddress:
        return self._email

    # NOTE: メールアドレスは後から変更可能(mutable)にしている
    @email.setter
    def email(self, email: "MailAddress"):
        if not isinstance(email, MailAddress):
            raise TypeError("email is not an instance of MailAddress")
        self._email = email

    def equals(self, user: "User"):
        if not isinstance(user, User):
            raise TypeError("user is not an instance of User")
        return self._id.value == user.id.value
