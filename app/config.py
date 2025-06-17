from pathlib import Path

from pydantic_settings import BaseSettings

from app.logs import logger

class Settings(BaseSettings):
    # Database settings
    sqlalchemy_database_uri: str
    sqlalchemy_echo: str

    # pylint: disable=too-few-public-methods
    class Config:
        env_file = Path(Path(__file__).resolve().parent.parent) / ".env"
        logger.info(f'environment created - {Path(Path(__file__).resolve().name)}')

settings = Settings()
