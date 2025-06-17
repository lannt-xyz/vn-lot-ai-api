from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings

connect_args = {}
debug_mode = settings.sqlalchemy_echo == settings.sqlalchemy_echo.lower()
engine = create_engine(settings.sqlalchemy_database_uri,
                       pool_size=20,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800,
                       echo=debug_mode,
                       connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

