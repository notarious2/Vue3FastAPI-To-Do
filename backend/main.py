from fastapi import FastAPI
from database import Base, engine
from routers import user, task, authorization
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()
Base.metadata.create_all(bind=engine)

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

# Create initialized database table
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)



@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/', tags=["root"])
async def root():
    return "Hello World!"




