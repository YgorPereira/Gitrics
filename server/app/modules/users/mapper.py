from app.entities.user_entity import UserEntity
from app.modules.users.models import UserModel


class UserMapper:
    @staticmethod
    def to_entity(user_model: UserModel) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            username=user_model.username,
            avatar_url=user_model.avatar_url,
            github_id=user_model.github_id,
            access_token=user_model.access_token,
            created_at=user_model.created_at,
        )

    @staticmethod
    def to_model(user_entity: UserEntity):

        return UserModel(
            id=user_entity.id,
            username=user_entity.username,
            avatar_url=user_entity.avatar_url,
            github_id=user_entity.github_id,
            access_token=user_entity.access_token,
            created_at=user_entity.created_at,
        )
