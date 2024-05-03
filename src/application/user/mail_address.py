from pydantic import BaseModel


class MailAddress(BaseModel, frozen=True):
    """メールアドレスの値オブジェクト(immutable)
    - TODO: メールアドレスの形式
    """

    value: str
