from uuid import UUID
from sqlalchemy import select

from app.entities import UserEntity
from app.modules.users.mapper import UserMapper

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import UserModel


class UserRepository:
    """
    Repository responsible for persisting and retrieving User data.

    This class encapsulates all direct database access for the User
    aggregate, translating between the persistence model (UserModel)
    and the domain entity (UserEntity) via UserMapper.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            db_session (AsyncSession): The active SQLAlchemy async session
            used to execute queries and persist changes.
        """
        self.db_session = db_session

    async def create_user(self, user: UserEntity) -> UserEntity:
        """
        Persist a new user in the database.

        Converts the given domain entity into a persistence model,
        adds it to the session, commits the transaction, and returns
        the persisted entity with any database-generated fields
        (e.g. id, created_at) populated.

        Args:
            user (UserEntity): The user entity to be created.

        Returns:
            UserEntity: The newly created user, including generated fields.
        """
        user_model = UserMapper.to_model(user)
        self.db_session.add(user_model)
        await self.db_session.commit()
        await self.db_session.refresh(user_model)
        return UserMapper.to_entity(user_model)

    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            UserEntity | None: The matching user entity, or None if no
            user with the given id exists.
        """
        result = await self.db_session.get(UserModel, user_id)

        if result is None:
            return None

        return UserMapper.to_entity(result)

    async def get_user_by_github_id(self, github_id: str) -> UserEntity | None:
        """
        Retrieve a user by their associated GitHub identifier.

        Args:
            github_id (str): The GitHub user id linked to the account.

        Returns:
            UserEntity | None: The matching user entity, or None if no
            user is linked to the given GitHub id.
        """
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.github_id == github_id)
        )
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return UserMapper.to_entity(user_model)

    async def update_user(self, user: UserEntity) -> UserEntity | None:
        """
        Update an existing user's data.

        Loads the current persistence model by id and overwrites all
        columns (except id and created_at) with the values from the
        given entity, then commits the change.

        Args:
            user (UserEntity): The user entity containing the updated data.
            Must include a valid id matching an existing record.

        Returns:
            UserEntity | None: The updated user entity, or None if no
            user with the given id exists.
        """
        user_model = await self.db_session.get(UserModel, user.id)

        if user_model is None:
            return None

        updated_data = UserMapper.to_model(user)
        for column in UserModel.__table__.columns.keys():
            if column in ("id", "created_at"):
                continue
            setattr(user_model, column, getattr(updated_data, column))

        await self.db_session.commit()
        await self.db_session.refresh(user_model)

        return UserMapper.to_entity(user_model)

    async def delete_user(self, user_id: UUID) -> bool:
        """
        Delete a user by their unique identifier.

        Args:
            user_id (UUID): The unique identifier of the user to delete.

        Returns:
            bool: True if the user was found and deleted, False if no
            user with the given id exists.
        """
        user_model = await self.db_session.get(UserModel, user_id)

        if user_model is None:
            return False

        await self.db_session.delete(user_model)
        await self.db_session.commit()

        return True