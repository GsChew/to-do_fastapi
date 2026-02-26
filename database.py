from fastapi.params import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, MappedAsDataclass
from sqlalchemy.sql.annotation import Annotated

DATABASE_URL = "postgresql+asyncpg://postgres@localhost:5432/taskflow"

engine = create_async_engine(DATABASE_URL, echo = True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with new_session as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]