from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database.models import Base
from config import DB_URL

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
