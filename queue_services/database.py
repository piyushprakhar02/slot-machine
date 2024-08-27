import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def getDBSession():
    dialect = os.getenv("DATABASE_DIALECT", "mysql+pymysql")
    username = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "secret")
    host = os.getenv("MYSQL_DB_HOST", "localhost")
    port = os.getenv("MYSQL_DB_PORT", "3306")
    database = os.getenv("MYSQL_DB", "userdb")

    connection_string = f"{dialect}://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()
