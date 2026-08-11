from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.users.services import UserServices
from app.entities.user_entity import UserEntity
from app.modules.users.exceptions import UserNotFoundException


@pytest.fixture()
def repository_mock():
    return AsyncMock()


@pytest.fixture()
def user_service(repository_mock):
    return UserServices(repository_mock)


class TestUserServices:
    @pytest.mark.unit
    async def test_create_user_service_should_return_created_user(
        self, user_service, make_user_entity, repository_mock
    ):
        random_id = uuid4()
        new_user = make_user_entity()

        created_user_mock = make_user_entity(id=random_id)
        repository_mock.create_user.return_value = created_user_mock

        created_user = await user_service.create_user(new_user)

        repository_mock.create_user.assert_called_once_with(user=new_user)
        assert isinstance(created_user, UserEntity)
        assert created_user.id == created_user_mock.id

    @pytest.mark.unit
    async def test_get_user_by_id_service_should_return_existent_user(
        self, user_service, make_user_entity, repository_mock
    ):
        random_uuid = uuid4()
        user_mock = make_user_entity(id=random_uuid)
        repository_mock.get_user_by_id.return_value = user_mock

        user = await user_service.get_user_by_id(random_uuid)

        repository_mock.get_user_by_id.assert_called_once_with(user_id=random_uuid)
        assert isinstance(user, UserEntity)
        assert user.id == random_uuid

    @pytest.mark.unit
    async def test_get_user_by_id_service_should_raise_not_found_exception_to_inexistent_user(
        self, user_service, repository_mock
    ):
        repository_mock.get_user_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            await user_service.get_user_by_id(uuid4())

        repository_mock.get_user_by_id.assert_called_once()

    @pytest.mark.unit
    async def test_get_user_by_github_id_service_should_return_existent_user(
        self, user_service, make_user_entity, repository_mock
    ):
        random_uuid = uuid4()
        user_mock = make_user_entity(id=random_uuid)
        repository_mock.get_user_by_github_id.return_value = user_mock

        user = await user_service.get_user_by_github_id(user_mock.github_id)

        repository_mock.get_user_by_github_id.assert_called_once_with(
            github_id=user_mock.github_id
        )
        assert isinstance(user, UserEntity)
        assert user == user_mock

    @pytest.mark.unit
    async def test_get_user_by_github_id_service_should_raise_not_found_exception_to_inexistent_user(
        self, user_service, repository_mock
    ):
        repository_mock.get_user_by_github_id.return_value = None

        with pytest.raises(UserNotFoundException):
            await user_service.get_user_by_github_id("1234")

        repository_mock.get_user_by_github_id.assert_called_once_with(github_id="1234")

    @pytest.mark.unit
    async def test_update_user_service_should_return_updated_user_data(
        self, user_service, make_user_entity, repository_mock
    ):
        random_uuid = uuid4()
        user_mock = make_user_entity(id=random_uuid)
        user_to_update = make_user_entity(
            id=random_uuid,
            username="updated_name",
            github_id="abcde",
            access_token="updatedtoken",
        )
        repository_mock.update_user.return_value = user_to_update

        user = await user_service.update_user(user_to_update)

        repository_mock.update_user.assert_called_once_with(user=user_to_update)
        assert isinstance(user, UserEntity)
        assert user.created_at == user_mock.created_at
        assert user.avatar_url == user_mock.avatar_url
        assert user.github_id == user_to_update.github_id
        assert user.username == user_to_update.username
        assert user.access_token == user_to_update.access_token

    @pytest.mark.unit
    async def test_update_user_service_should_raise_not_found_exception_to_inexistent_user(
        self, user_service, repository_mock, make_user_entity
    ):
        repository_mock.update_user.return_value = None
        user_mock = make_user_entity(id=uuid4())

        with pytest.raises(UserNotFoundException):
            await user_service.update_user(user_mock)

        repository_mock.update_user.assert_called_once_with(user=user_mock)
