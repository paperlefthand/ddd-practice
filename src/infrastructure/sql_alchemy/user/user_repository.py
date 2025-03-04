from typing import Optional

from application.user.mail_address import MailAddress
from domain.models.user.iuser_repository import IUserRepository
from domain.models.user.user import User, UserId, UserName
from injector import inject
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SQLAlchemyUserRepository(IUserRepository):
    # NOTE: sessionはwithコンテキストで管理する方法もあるが,
    # あえてtry~catchで明示している
    @inject
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    class UserDataModel(Base):
        # NOTE __tablename__はCase Sensitive
        __tablename__ = "user"
        id = Column(String(32), primary_key=True)
        name = Column(String(32))
        email = Column(String(50))

        def __repr__(self):
            return f"<User(id={self.id}, name={self.name}, email={self.email})>"

    # TODO UserDataModelモデルからUserへ変換する関数
    # TODO user_factoryの利用

    def find_by_name(self, name: "UserName") -> list["User"]:
        session = self.session_factory()
        try:
            results = session.query(self.UserDataModel).filter_by(name=name.value).all()
            session.commit()
            return [
                User(
                    id=UserId(value=result.id),
                    name=UserName(value=result.name),
                    email=MailAddress(value=result.email),
                )
                for result in results
            ]
        finally:
            session.close()

    def find_by_id(self, id: "UserId") -> Optional["User"]:
        session = self.session_factory()
        try:
            result = session.query(self.UserDataModel).filter_by(id=id.value).first()
            session.commit()
            return (
                User(
                    id=UserId(value=result.id),
                    name=UserName(value=result.name),
                    email=MailAddress(value=result.email),
                )
                if bool(result)
                else None
            )
        finally:
            session.close()

    def find_by_email(self, email: MailAddress) -> Optional["User"]:
        session = self.session_factory()
        try:
            result = (
                session.query(self.UserDataModel).filter_by(email=email.value).first()
            )
            return (
                User(
                    id=UserId(value=result.id),
                    name=UserName(value=result.name),
                    email=MailAddress(value=result.email),
                )
                if bool(result)
                else None
            )
        finally:
            session.close()

    def delete(self, user: "User"):
        session = self.session_factory()
        try:
            result = (
                session.query(self.UserDataModel).filter_by(id=user.id.value).first()
            )
            if result:
                session.delete(result)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def save(self, user: "User"):
        session = self.session_factory()
        try:
            result = (
                session.query(self.UserDataModel).filter_by(id=user.id.value).first()
            )
            if result:
                result.name = user.name.value
                result.email = user.email.value
            else:
                result = self.UserDataModel(
                    id=user.id.value, name=user.name.value, email=user.email.value
                )
                session.add(result)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
