import pytest
from fullname import FullName
from pydantic import ValidationError


@pytest.mark.parametrize(
    "first_name, last_name",
    [(123, "Doe"), ("John", None), ("John", "DOE"), ("john", "Doe"), ("123", "Doe")],
)
def test_init_validation_error(first_name, last_name):
    with pytest.raises(ValidationError):
        FullName(first_name=first_name, last_name=last_name)


def test_equals():
    a = FullName(first_name="John", last_name="Doe")
    b = FullName(first_name="John", last_name="Doe")
    assert a.equals(b)


def test_not_equals():
    a = FullName(first_name="John", last_name="Doe")
    b = FullName(first_name="Jane", last_name="Doe")
    assert not a.equals(b)


@pytest.mark.parametrize("invalid_value", [1, None])
def test_equals_type_error(invalid_value):
    a = FullName(first_name="John", last_name="Doe")
    with pytest.raises(TypeError):
        a.equals(invalid_value)


def test_immutability():
    a = FullName(first_name="John", last_name="Doe")
    with pytest.raises(ValidationError):
        a.first_name = "Jane"  # type: ignore


def test_update_last_name():
    a = FullName(first_name="John", last_name="Doe")
    b = a.update_last_name("Smith")
    assert b.equals(FullName(first_name="John", last_name="Smith"))
