from application.user.user_register_service import UserRegisterCommand
from domain.models.user.user import UserName


def test_user_register(user_register_service, user_repository):
    command = UserRegisterCommand(name="XXXX", email="XXXXXXXXXXXXX")
    user_register_service.handle(command)
    assert len(user_repository.find_by_name(UserName(value="XXXX"))) == 1
