from sqlalchemy import Column, String, DateTime, Integer, func, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    birthdate = Column(Date)
    last_login_at = Column(DateTime)

    def __repr__(self):
        return f'<User {self.email}>'


class Token(Base):
    __tablename__ = "tokens"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    balance = Column('balance', Integer)


class SlotMachine(Base):
    __tablename__ = 'slot_machine'

    id = Column('id', String, primary_key=True)
    name = Column('name', String, unique=True, nullable=False)
    balance = Column('balance', Integer, nullable=False)
    status = Column('status', String)
