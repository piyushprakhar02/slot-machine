import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.repositories.user_repository import UserRepository
from datetime import datetime, date

# Assume your database URL is set in your environment
DATABASE_URL = "mysql+pymysql://root:secret@localhost/userdb"

# Create engine and session for testing
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for testing (ensure tables are present)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a new database session for each test."""
    session = SessionLocal()
    try:
        yield session
        session.rollback()  # Rollback any changes after the test
    finally:
        session.close()


@pytest.fixture(scope="function")
def user_repository(db):
    return UserRepository(db)


def test_add_user(user_repository, db):
    user = user_repository.add_user(id="123", email="test@example.com", name="Test User", birthdate="2024-08-19")
    assert user.id == "123"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.birthdate == date(2024, 8, 19)


def test_get_user(user_repository, db):
    user = user_repository.get_user(email="test@example.com")
    assert user.email == "test@example.com"


def test_update_user(user_repository, db):
    updated_user = user_repository.update_user(email="test@example.com", data={"name": "Updated Name"})
    assert updated_user.name == "Updated Name"
