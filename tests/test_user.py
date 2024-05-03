import pytest
from application.user.mail_address import MailAddress
from domain.models.user.user import User, UserId, UserName
from pydantic import ValidationError

UID_0 = UserId(value="001")
UNAME_0 = UserName(value="john")
EMAIL_0 = MailAddress(value="xxx@mail.example.com")


def test_equals():
    """オブジェクトとして別物で,nameを変更してもidが等しければ同一判定"""
    uid = UserId(value="001")
    a = User(id=uid, name=UNAME_0, email=EMAIL_0)
    b = User(id=uid, name=UNAME_0, email=EMAIL_0)
    assert id(a) != id(b)
    a.change_name(UserName(value="jane"))
    assert a.name != b.name
    assert a.equals(b)


def test_userid_immutability():
    """ユーザIDは変更不可"""
    a = User(id=UserId(value="001"), name=UNAME_0, email=EMAIL_0)
    with pytest.raises(ValidationError):
        a.id = UserId(value="002")  # type: ignore


def test_username_mutability():
    """ユーザ名は変更可"""
    a = User(id=UID_0, name=UserName(value="john"), email=EMAIL_0)
    a.change_name(UserName(value="jane"))
    assert a.name.value == "jane"


def test_init_user_id_str():
    with pytest.raises(AssertionError):
        User(id="001", name=UNAME_0, email=EMAIL_0)  # type: ignore


def test_init_user_id_none():
    with pytest.raises(AssertionError):
        User(id=None, name=UNAME_0, email=EMAIL_0)  # type: ignore


# TODO このへんパラメータ化
def test_init_user_id_invalid_type():
    with pytest.raises(AssertionError):
        User(id=UserName(value="john"), name=UNAME_0, email=EMAIL_0)  # type: ignore


def test_init_user_name_none():
    with pytest.raises(TypeError):
        User(name=None, email=EMAIL_0)  # type: ignore


def test_init_user_name_invalid_type():
    with pytest.raises(TypeError):
        User(name=UserId(value="john"), email=EMAIL_0)  # type: ignore


"""
 TODO テストパターン
- 文字数
- email形式
"""
