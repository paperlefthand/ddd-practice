import uuid

from application.user.mail_address import MailAddress
from domain.models.user.iuser_factory import IUserFactory
from domain.models.user.user import User, UserId, UserName


class UserFactory(IUserFactory):
    """新規UserはこのFactory経由で作成する"""

    # HACK: ユーザIDの仕様で決められた制限文字数が32文字未満の場合UUIDが使えない.どうするか.
    # ->idはあくまで内部で使う識別子.ユーザが認識する識別子はemailとするかもしくは別のidを追加.

    def create(self, name: UserName, email: MailAddress):
        # NOTE 型アサーション.これに引っかかるということはプログラムミスの可能性が高い.
        # 実際にNone等が入ることが仕様として起こりえるならそれ特有の例外を発生される.
        assert isinstance(name, UserName)
        assert isinstance(email, MailAddress)
        # NOTE UUIDによる採番としたが,リポジトリ経由で連番を取得して設定してもよい.
        id = UserId(value=str(uuid.uuid4()).replace("-", ""))
        return User(id=id, name=name, email=email)
