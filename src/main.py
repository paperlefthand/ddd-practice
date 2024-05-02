# %%
from application.user_register_service import UserRegisterCommand, UserRegisterService
from application.user_update_info_service import (
    UserUpdateCommand,
    UserUpdateInfoService,
)
from injector import Injector, Module, provider, singleton
from iuser_factory import IUserFactory
from iuser_repository import IUserRepository
from mail_address import MailAddress
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from user import User, UserName
from user_domain_service import UserDomainService
from user_factory import UserFactory
from user_repository import SQLAlchemyUserRepository

# %%


class RepositoryModule(Module):
    # インターフェースに対する具象クラスの引き当て
    def configure(self, binder):
        binder.bind(IUserRepository, to=SQLAlchemyUserRepository)

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
        binder.install(RepositoryModule)
        binder.bind(IUserFactory, to=UserFactory)
        # binder.bind(UserRegisterService)


def main():
    injector = Injector(modules=[ApplicationModule()])
    user_register_service = injector.get(UserRegisterService)
    result = user_register_service.handle(
        UserRegisterCommand(name="taro", email="zzz@mail.example.com")
    )
    print(result)


# %%
main()
# %%


# データベースへの接続エンジンを設定
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:15432/postgres"
)
# sessionmakerはSessionオブジェクトのファクトリを作成する.
Session = sessionmaker(bind=engine)
session = Session()

user_repo = SQLAlchemyUserRepository(session)
user_service = UserDomainService(user_repo)

# %%

user_name = UserName(value="taro")
user_email = MailAddress(value="xxx@mail.example.com")
new_user = User(name=user_name, email=user_email)

user_repo.save(new_user)
# res = user_service.exists(user_name)

res = user_repo.find_by_id(id=new_user.id)
if res is not None:
    res.name = UserName(value="jiro")
    user_repo.save(res)


user_name = UserName(value="kogoro")
res = user_repo.find_by_name(user_name)
print(res)

# %%

user_update_service = UserUpdateInfoService(
    user_repository=user_repo, user_domain_service=user_service
)

update_name_command = UserUpdateCommand(
    id="e589f1e7d8474c58b1044c7fe0aec154", name="john"
)
try:
    user_update_service.handle(update_name_command)
except Exception as e:
    print(e)

update_email_command = UserUpdateCommand(
    id="fc15304a07f440bbacfe76227aea3330", email="yyy@mail.example.com"
)
try:
    user_update_service.handle(update_email_command)
except Exception as e:
    print(e)

# %%
