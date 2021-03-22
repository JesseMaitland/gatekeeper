from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

MODEL_CONFIG = {"schema": "gatekeeper"}

Base = declarative_base()


class UserData(Base):
    __tablename__ = 'users'
    __table_args__ = MODEL_CONFIG

    name = Column(String(100), nullable=False, primary_key=True)
    hash_value = Column(String(250), nullable=True, unique=True)
    state = Column(String(100), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), nullable=True)

    @staticmethod
    def save_users(users: List['ObjectState'], session) -> None:
        for user in users:
            session.add(user)
        session.commit()


class Secrets(Base):
    __tablename__ = 'secrets'
    __table_args__ = MODEL_CONFIG

    name = Column(String(100), nullable=False, primary_key=True)
    state = Column(String(100), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), nullable=True)

    @staticmethod
    def get_fernet_key_state(session) -> 'Secrets':
        statement = select(Secrets).where(Secrets.name == 'secret_key')
        result = session.execute(statement).first()
        return result[0] if result else None

    @staticmethod
    def save_key_state(key_state: 'Secrets', session) -> None:
        session.add(key_state)
        session.commit()
