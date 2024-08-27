from sqlalchemy import Column, String, DateTime, Date, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    birthdate = Column(Date)
    last_login_at = Column(DateTime, default=func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'
