import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database(model):
    model.metadata.drop_all(bind=engine)
    model.metadata.create_all(bind=engine)


class SessionContextManager:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.db_session: Session = None

    def __enter__(self):
        self.db_session = self.session_factory()
        return self.db_session

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db_session:
            self.db_session.close()


def get_database_session() -> SessionContextManager:
    return SessionContextManager(SessionLocal)
