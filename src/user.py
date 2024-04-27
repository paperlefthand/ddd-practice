# %%


from pydantic import BaseModel, Field


class UserId(BaseModel, frozen=True):
    value: str = Field(pattern=r".+")


class UserName(BaseModel, frozen=True):
    value: str = Field(pattern=r".{3}.*")


class User:
    def __init__(self, id: UserId, name: UserName):
        self._id: UserId = id
        self._name: UserName = name

    # NOTE getterのみ定義することでユーザIDをimmutableにしている
    @property
    def id(self) -> UserId:
        return self._id

    @property
    def name(self) -> UserName:
        return self._name

    # NOTE ユーザ名は後から変更可能にしている
    @name.setter
    def name(self, name: "UserName"):
        if not isinstance(name, UserName):
            raise TypeError("name is not UserName")
        self._name = name

    def equals(self, user: "User"):
        if not isinstance(user, User):
            raise TypeError("user is not User")
        return self._id.value == user.id.value


uid = UserId(value="sssf")
uname = UserName(value="sssf")
user = User(id=uid, name=uname)
# user.id = UserId(value="s")

# %%
