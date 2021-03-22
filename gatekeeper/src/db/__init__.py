import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


class RedshiftClient:

    def __init__(self, connection_name: str) -> None:
        self.connection_name = connection_name
        self.engine = create_engine(os.getenv(self.connection_name, self.connection_name))

    def create_schema(self) -> None:
        self.engine.execute("CREATE SCHEMA IF NOT EXISTS gatekeeper;")

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
