from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'sqlite:///./sqlite_db.db'


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()