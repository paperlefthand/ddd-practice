from typing import Optional

from iuser_repository import IUserRepository
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from user import User, UserId, UserName

Base = declarative_base()


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    class UserDataModel(Base):
        # NOTE __tablename__はCase Sensitive
        __tablename__ = "user"
        id = Column(String(32), primary_key=True)
        name = Column(String(32))

    def find_by_name(self, name: "UserName") -> list["User"]:
        results = (
            self.session.query(self.UserDataModel).filter_by(name=name.value).all()
        )
        return [
            User(id=UserId(value=result.id), name=UserName(value=result.name))
            for result in results
        ]

    def find_by_id(self, id: "UserId") -> Optional["User"]:
        result = self.session.query(self.UserDataModel).filter_by(id=id.value).first()
        return (
            User(id=UserId(value=result.id), name=UserName(value=result.name))
            if bool(result)
            else None
        )

    def add(self, user: "User"):
        result = self.UserDataModel(id=user.id.value, name=user.name.value)
        self.session.add(result)
        self.session.commit()

    def delete(self, user: "User"):
        result = (
            self.session.query(self.UserDataModel).filter_by(id=user.id.value).first()
        )
        if result:
            self.session.delete(result)
            self.session.commit()

    def save(self, user: "User"):
        result = (
            self.session.query(self.UserDataModel).filter_by(id=user.id.value).first()
        )
        if result:
            result.name = user.name.value
        else:
            result = self.UserDataModel(id=user.id.value, name=user.name.value)
            self.session.add(result)
        self.session.commit()
