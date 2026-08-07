from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from app.core.database import Base
from app.core.mixins import IdMixin


class UserModel(Base, IdMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    access_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(100), nullable=False)
