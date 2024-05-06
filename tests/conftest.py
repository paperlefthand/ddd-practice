import pytest
from application.user.user_register_service import UserRegisterService
from domain.services.user_domain_service import UserDomainService
from infrastructure.mock.user.user_mock_repository import UserMockRepository
from infrastructure.user_factory import UserFactory


@pytest.fixture(scope="session")
def user_repository():
    return UserMockRepository()


@pytest.fixture(scope="session")
def user_register_service(user_repository):
    domain_service = UserDomainService(user_repository)
    factory = UserFactory()

    return UserRegisterService(
        user_repository=user_repository,
        user_domain_service=domain_service,
        user_factory=factory,
    )
