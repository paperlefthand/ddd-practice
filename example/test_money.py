import pytest
from pydantic import ValidationError

from example.money import Money


def test_init_validation_error():
    with pytest.raises(ValidationError):
        Money(amount=-1, currency="USD")
    with pytest.raises(ValidationError):
        Money(amount=1, currency="円")


def test_add():
    assert Money(amount=1, currency="USD") + Money(amount=2, currency="USD") == Money(
        amount=3, currency="USD"
    )
    assert Money(amount=1, currency="JPY") + Money(amount=2, currency="JPY") == Money(
        amount=3, currency="JPY"
    )


def test_add_type_error():
    with pytest.raises(TypeError):
        Money(amount=1, currency="USD") + "test"  # type: ignore


def test_add_value_error():
    with pytest.raises(ValueError):
        _ = Money(amount=1, currency="USD") + Money(amount=2, currency="JPY")


def test_immutability():
    m = Money(amount=1, currency="USD")
    with pytest.raises(ValidationError):
        m.amount = 2  # type: ignore
