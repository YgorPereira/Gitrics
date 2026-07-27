from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core import settings

engine = create_async_engine(
    url=settings.database_url,
    echo=settings.DEBUG,
)

SessionFactory = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)
