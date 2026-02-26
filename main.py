from fastapi import FastAPI
from app.models import User, Task
from app.database import SessionDep, engine, Base

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database is ready')
    yield
    print('End')

app = FastAPI(lifespan=lifespan)