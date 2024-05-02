from pydantic import BaseModel, Field


class Money(BaseModel, frozen=True):
    amount: int = Field(ge=0)
    currency: str = Field(pattern=r"[A-Z]{3}")

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError("Can only add Money objects")
        if self.currency != other.currency:
            raise ValueError("Currencies must match")
        return Money(amount=self.amount + other.amount, currency=self.currency)
