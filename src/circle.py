from pydantic import BaseModel, Field
from user import User


class CircleId(BaseModel):
    value: str = Field(min_length=3, max_length=32)


class CircleName(BaseModel):
    value: str = Field(min_length=3, max_length=20)

    def equals(self, other):
        return self.value == other.value


class Circle:
    def __init__(
        self,
        id: CircleId,
        name: CircleName,
        owner: User,
        members: list[User],
    ):
        self.id = id
        self.name = name
