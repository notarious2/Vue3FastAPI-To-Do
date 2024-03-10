from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.database import engine
from backend.models import metadata
from backend.routers import authorization, task, user


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables() -> None:
    metadata.bind = engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
