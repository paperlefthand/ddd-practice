from application.user.user_register_service import (
    UserRegisterCommand,
    UserRegisterService,
)
from domain.models.user.iuser_factory import IUserFactory
from domain.models.user.iuser_repository import IUserRepository
from infrastructure.sql_alchemy.user.user_repository import SQLAlchemyUserRepository
from infrastructure.user_factory import UserFactory
from injector import Injector, Module, provider, singleton
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

# NOTE Moduleの依存関係ツリーはクラス図を参照して設計する


class InfrastructureModule(Module):
    # NOTE: インターフェースに対する具象クラスの引き当て
    # Singletonスコープのため,一度インスタンスが生成されたら使いまわされる
    def configure(self, binder):
        binder.bind(IUserRepository, to=SQLAlchemyUserRepository, scope=singleton)

    @singleton
    @provider
    def provide_engine(self) -> Engine:
        return create_engine(
            "postgresql+psycopg2://postgres:postgres@localhost:15432/postgres"
        )

    # NOTE 依存オブジェクト(ここではシングルトン)のファクトリの役割
    # 生成に関する知識(どのDBエンジンを使うか)を有する.
    @singleton
    @provider
    def provide_session_factory(self, engine: Engine) -> sessionmaker:
        return sessionmaker(bind=engine)


class ApplicationModule(Module):
    def configure(self, binder):
        binder.install(InfrastructureModule)
        binder.bind(IUserFactory, to=UserFactory, scope=singleton)


def main():
    injector = Injector(modules=[ApplicationModule()])
    # NOTE: injector(DIコンテナ)を経由することで,
    # bindやinstallで指定した依存オブジェクトが設定されたUserRegisterServiceのインスタンスを取得できる.
    user_register_service = injector.get(UserRegisterService)
    result = user_register_service.handle(
        UserRegisterCommand(name="taro", email="zzz@mail.example.com")
    )
    print(result)


if __name__ == "__main__":
    main()
