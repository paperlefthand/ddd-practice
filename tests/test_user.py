import pytest
from user import User, UserId, UserName


def test_equals():
    """オブジェクトとして別物で,nameを変更してもidが等しければ同一判定"""
    uid = UserId(value="001")
    uname = UserName(value="john")
    a = User(id=uid, name=uname)
    b = User(id=uid, name=uname)
    assert id(a) != id(b)
    a.name = UserName(value="jane")
    assert a.name != b.name
    assert a.equals(b)


def test_userid_immutability():
    """ユーザIDは変更不可"""
    uname = UserName(value="john")
    a = User(name=uname)
    with pytest.raises(AttributeError):
        a.id = UserId(value="001")  # type: ignore


def test_username_mutability():
    """ユーザ名は変更可"""
    uname = UserName(value="john")
    a = User(name=uname)
    a.name = UserName(value="jane")
    assert a.name.value == "jane"


def test_init_user_id_str():
    with pytest.raises(TypeError):
        User(id="001", name=UserName(value="john"))  # type: ignore


def test_init_user_id_none():
    with pytest.raises(TypeError):
        User(id=None, name=UserName(value="john"))  # type: ignore


def test_init_user_id_invalid_type():
    with pytest.raises(TypeError):
        User(id=UserName(value="john"), name=UserName(value="doh"))  # type: ignore


def test_init_user_name_none():
    with pytest.raises(TypeError):
        User(name=None)  # type: ignore


def test_init_user_name_invalid_type():
    with pytest.raises(TypeError):
        User(name=UserId(value="john"))  # type: ignore
