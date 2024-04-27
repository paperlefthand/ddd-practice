import pytest
from user import User, UserId, UserName


def test_equals():
    uid = UserId(value="001")
    uname = UserName(value="john")
    a = User(uid, uname)
    b = User(uid, uname)
    assert id(a) != id(b)
    a.name = UserName(value="jane")
    assert a.name != b.name
    assert a.equals(b)


def test_userid_immutability():
    uid = UserId(value="001")
    uname = UserName(value="john")
    a = User(uid, uname)
    with pytest.raises(AttributeError):
        a.id = UserId(value="002")  # type: ignore


def test_username_mutability():
    uid = UserId(value="001")
    uname = UserName(value="john")
    a = User(uid, uname)
    a.name = UserName(value="jane")
    assert a.name.value == "jane"
