from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core import settings

engine = create_async_engine(
    url=settings.database_url,
    echo=settings.DEBUG,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for all models."""

    pass
