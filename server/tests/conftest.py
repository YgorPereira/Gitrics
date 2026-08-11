import os
from typing import Any, Callable, cast

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import pytest
from pytest_postgresql.janitor import DatabaseJanitor

from app.core.database import AsyncSessionFactory, Base
from app.models import *
from app.core.dependencies import get_db
from app.entities.user_entity import UserEntity


@pytest.fixture()
def temp_postgre_db():
    """
    Fixture to create a temporary PostgreSQL database for testing.
    This fixture will create a new database, yield its connection string,
    and then drop the database after the test is done.
    """
    with DatabaseJanitor(
        user=os.environ.get("PSGRE_USER", "postgres"),
        host=os.environ.get("PSGRE_HOST", "localhost"),
        port=os.environ.get("PSGRE_PORT", 5432),
        dbname=os.environ.get("PSGRE_DB", "gitrics"),
        password=os.environ.get("PSGRE_PASSWORD", "secret_password"),
        version=15,
    ) as janitor:
        yield f"postgresql+asyncpg://{janitor.user}:{janitor.password}@{janitor.host}:{janitor.port}/{janitor.dbname}"


@pytest_asyncio.fixture()
async def test_db_engine(temp_postgre_db):
    engine = create_async_engine(temp_postgre_db, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture()
async def db_session(test_db_engine):
    AsyncSessionFactory.configure(bind=test_db_engine)
    async for session in get_db():
        yield session
        await session.rollback()


@pytest.fixture
def make_user_entity() -> Callable[..., UserEntity]:
    def _make(**overrides: Any) -> UserEntity:
        data = dict(
            id=None,
            github_id="123456",
            username="testuser",
            avatar_url="https://example.com/avatar.png",
            access_token="testaccesstoken",
            created_at="2023-01-01T00:00:00Z",
        )
        data.update(overrides)
        return UserEntity(**cast(dict[str, Any], data))

    return _make
