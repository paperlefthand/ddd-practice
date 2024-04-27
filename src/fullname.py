# %%

from pydantic import BaseModel, Field

NAME_PATTERN = r"^[A-Z][a-z]+$"


class FullName(BaseModel, frozen=True):
    first_name: str = Field(pattern=NAME_PATTERN)
    last_name: str = Field(pattern=NAME_PATTERN)

    def equals(self, other: "FullName") -> bool:
        if not isinstance(other, FullName):
            raise TypeError("other is not FullName")
        else:
            return (
                self.first_name == other.first_name
                and self.last_name == other.last_name
            )

    def update_last_name(self, last_name: str) -> "FullName":
        return FullName(first_name=self.first_name, last_name=last_name)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


p = FullName(first_name="Taro", last_name="Yamada")
print(p.model_dump())
q = p.update_last_name(last_name="Suzuki")
print(q.model_dump())

# %%
