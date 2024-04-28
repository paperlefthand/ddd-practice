# %%
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User, UserName
from user_repository import SQLAlchemyUserRepository
from user_service import UserService

# データベースへの接続エンジンを設定
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:15432/postgres"
)
# セッションメーカーを設定
Session = sessionmaker(bind=engine)
session = Session()

user_repo = SQLAlchemyUserRepository(session)
user_service = UserService(user_repo)

# %%

user_name = UserName(value="taro")
new_user = User(name=user_name)

user_repo.save(new_user)
# res = user_service.exists(user_name)

res = user_repo.find_by_id(id=new_user.id)
if res is not None:
    res.name = UserName(value="jiro")
    user_repo.save(res)


# %%

user_name = UserName(value="kogoro")
res = user_repo.find_by_name(user_name)
res

# %%
