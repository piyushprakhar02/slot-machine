from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
import os

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:"
    f"{os.getenv('MYSQL_PASSWORD', 'secret')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/"
    f"{os.getenv('MYSQL_DB', 'userdb')}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)

    @app.on_event("shutdown")
    async def shutdown():
        pass


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
