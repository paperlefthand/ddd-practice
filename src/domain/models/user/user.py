from application.user.mail_address import MailAddress
from pydantic import BaseModel, Field, PrivateAttr


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


class User(BaseModel):
    """ユーザエンティティ
    - ユーザIDはimmutable, ユーザ名とメールアドレスはメソッドを介して変更可能.
    """

    id: UserId = Field(frozen=True)
    _name: UserName = PrivateAttr()
    _email: MailAddress = PrivateAttr()

    def __init__(
        self,
        id: UserId,
        name: UserName,
        email: MailAddress,
    ):
        # NOTE 型アサーション. これに引っかかるということはプログラムミスの可能性が高い.
        assert isinstance(id, UserId)
        assert isinstance(name, UserName)
        assert isinstance(email, MailAddress)
        super().__init__(id=id)
        self._name: UserName = name
        self._email: MailAddress = email

    @property
    def name(self) -> UserName:
        return self._name

    def change_name(self, name: UserName):
        # NOTE: setterではなく"ユーザ名の変更"という自然な言葉を使う(ユビキタスを意識)
        if not isinstance(name, UserName):
            raise TypeError("name is not an instance of UserName")
        self._name = name

    @property
    def email(self) -> MailAddress:
        return self._email

    def change_email(self, email: MailAddress):
        # NOTE: setterではなく"メールアドレスの変更"という自然な言葉を使う(ユビキタスを意識)
        if not isinstance(email, MailAddress):
            raise TypeError("email is not an instance of MailAddress")
        self._email = email

    def equals(self, user: "User"):
        if not isinstance(user, User):
            raise TypeError("user is not an instance of User")
        return self.id.value == user.id.value

    def is_premium(self) -> bool:
        # TODO 実装
        return False
