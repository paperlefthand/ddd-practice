from user import User


class UserData:
    """アプリケーションサービス外部への受け渡し用DTO
    - NOTE: フィールドが変更されたときのために, コンストラクタには個々の引数ではなく,
      Userオブジェクトを直接受け取るようにしている
    """

    def __init__(self, user: User) -> None:
        self.id = user.id.value
        self.name = user.name.value
        self.email = user.email.value
