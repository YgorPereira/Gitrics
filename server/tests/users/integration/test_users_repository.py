import pytest

from app.entities import UserEntity
from app.modules.users.repository import UserRepository


@pytest.fixture
def user_repository(db_session) -> UserRepository:
    return UserRepository(db_session=db_session)


@pytest.fixture
def make_user_entity() -> UserEntity:
    def _make(**overrides) -> UserEntity:
        data = dict(
            id=None,
            github_id="123456",
            username="testuser",
            avatar_url="https://example.com/avatar.png",
            access_token="testaccesstoken",
            created_at="2023-01-01T00:00:00Z",
        )
        data.update(overrides)
        return UserEntity(**data)

    return _make


class TestUserRepository:
    @pytest.mark.integration
    async def test_create_user_should_create_successfully(
        self, user_repository, make_user_entity
    ):
        created_user = await user_repository.create_user(make_user_entity())

        assert created_user.id is not None
        assert created_user.username == "testuser"
        assert created_user.github_id == "123456"
        assert created_user.avatar_url == "https://example.com/avatar.png"
        assert created_user.access_token == "testaccesstoken"
        assert created_user.created_at == "2023-01-01T00:00:00Z"
        assert isinstance(created_user, UserEntity)

    @pytest.mark.integration
    async def test_get_user_by_id_should_return_existent_user(
        self, user_repository, make_user_entity
    ):
        created_user = await user_repository.create_user(
            make_user_entity(github_id="123457", username="octopuscat")
        )

        founded_user = await user_repository.get_user_by_id(created_user.id)

        assert founded_user.id == created_user.id
        assert founded_user.username == created_user.username
        assert founded_user.github_id == created_user.github_id
        assert founded_user.avatar_url == created_user.avatar_url
        assert founded_user.access_token == created_user.access_token
        assert founded_user.created_at == created_user.created_at
        assert isinstance(founded_user, UserEntity)

    @pytest.mark.integration
    async def test_get_user_by_github_id_should_return_existent_user(
        self, user_repository, make_user_entity
    ):
        created_user = await user_repository.create_user(
            make_user_entity(github_id="123458", username="linus_torvald")
        )

        founded_user = await user_repository.get_user_by_github_id(
            created_user.github_id
        )

        assert founded_user.id == created_user.id
        assert founded_user.username == created_user.username
        assert founded_user.github_id == created_user.github_id
        assert founded_user.avatar_url == created_user.avatar_url
        assert founded_user.access_token == created_user.access_token
        assert founded_user.created_at == created_user.created_at
        assert isinstance(founded_user, UserEntity)

    @pytest.mark.integration
    async def test_update_user_should_update_successfully(
        self, user_repository, make_user_entity
    ):
        created_user = await user_repository.create_user(
            make_user_entity(
                github_id="3459",
                username="crazy_react_dev",
                avatar_url="https://example.com/aang.png",
            )
        )

        data_to_update = dict(
            id=created_user.id,
            github_id="420",
            username="herb_senior",
            avatar_url="https://example.com/mariajuana.png",
        )

        updated_user = await user_repository.update_user(
            make_user_entity(**data_to_update)
        )

        assert updated_user.id == created_user.id
        assert updated_user.github_id == data_to_update["github_id"]
        assert updated_user.username == data_to_update["username"]
        assert updated_user.avatar_url == data_to_update["avatar_url"]
        assert updated_user.access_token == created_user.access_token
        assert updated_user.created_at == created_user.created_at

    @pytest.mark.integration
    async def test_delete_user_should_delete_successfully(
        self, user_repository, make_user_entity
    ):
        created_user = await user_repository.create_user(make_user_entity())

        delete_result = await user_repository.delete_user(created_user.id)

        founded_user = await user_repository.get_user_by_id(created_user.id)

        assert delete_result is True
        assert founded_user is None
