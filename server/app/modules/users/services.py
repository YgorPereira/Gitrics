from uuid import UUID


from app.entities.user_entity import UserEntity
from app.modules.users.exceptions import UserNotFoundException
from app.modules.users.repository import UserRepository
from app.core.crypto import encrypt_token


class UserService:
    """
    Service layer responsible for user-related business rules.

    Coordinates with UserRepository to fetch and persist user data,
    and enforces domain rules such as raising UserNotFoundException
    when an expected user does not exist.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the service with a user repository.

        Args:
            repository (UserRepository): The repository used to access
            and persist user data.
        """
        self.repository = repository

    async def create_user(self, user: UserEntity) -> UserEntity:
        """
        Create a new user.

        Args:
            user (UserEntity): The user entity to be created.

        Returns:
            UserEntity: The newly created user, including generated fields.
        """
        return await self.repository.create_user(user=user)

    async def get_user_by_id(self, user_id: UUID) -> UserEntity:
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            UserEntity: The matching user entity.

        Raises:
            UserNotFoundException: If no user with the given id exists.
        """
        user = await self.repository.get_user_by_id(user_id=user_id)

        if user is None:
            raise UserNotFoundException()

        return user

    async def get_user_by_github_id(self, github_id: str) -> UserEntity:
        """
        Retrieve a user by their associated GitHub identifier.

        Args:
            github_id (str): The GitHub user id linked to the account.

        Returns:
            UserEntity: The matching user entity.

        Raises:
            UserNotFoundException: If no user is linked to the given
            GitHub id.
        """
        user = await self.repository.get_user_by_github_id(github_id=github_id)

        if user is None:
            raise UserNotFoundException()

        return user

    async def update_user(self, user: UserEntity) -> UserEntity:
        """
        Update an existing user's data.

        Args:
            user (UserEntity): The user entity containing the updated data.
            Must include a valid id matching an existing record.

        Returns:
            UserEntity: The updated user entity.

        Raises:
            UserNotFoundException: If no user with the given id exists.
        """
        updated_user = await self.repository.update_user(user=user)

        if updated_user is None:
            raise UserNotFoundException()

        return updated_user

    async def get_and_update_or_create_user(
        self, github_id: str, github_user: dict, access_token: str
    ) -> UserEntity:
        """
        ...
        """
        encrypted_token = encrypt_token(access_token)

        try:
            user = await self.get_user_by_github_id(github_id=github_id)
            user.username = github_user.get("username")  # type: ignore
            user.avatar_url = github_user.get("avatar_url")
            user.access_token = encrypted_token
            return await self.update_user(user=user)
        except UserNotFoundException:
            new_user = UserEntity(
                github_id=github_id,
                username=github_user.get("username"),  # type: ignore
                avatar_url=github_user.get("avatar_url"),
                access_token=encrypted_token,
            )
            return await self.create_user(user=new_user)
