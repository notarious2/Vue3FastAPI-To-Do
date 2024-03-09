from fastapi import FastAPI
from database import engine
from models import BaseModel
from routers import user, task, authorization
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(task.router)
app.include_router(authorization.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)








