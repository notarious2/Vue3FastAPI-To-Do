from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.database import engine
from backend.models import metadata
from backend.routers import authentication, task, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(task.router)
app.include_router(authentication.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/login", include_in_schema=False)
async def login_page(request: Request):
    return RedirectResponse(url="/", status_code=302)


@app.get("/register", include_in_schema=False)
async def register_page(request: Request):
    return RedirectResponse(url="/", status_code=302)


@app.get("/callback", include_in_schema=False)
async def callback_page(request: Request):
    return RedirectResponse(url="/", status_code=302)


async def create_tables() -> None:
    metadata.bind = engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
