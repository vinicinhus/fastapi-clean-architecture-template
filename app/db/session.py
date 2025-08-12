from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.core.logging import logger

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Enable SQLModel echo logs if set to True
    pool_pre_ping=True,  # Helps to check if the connection is alive before using it
)


def init_db() -> None:
    """
    Initialize the database by creating all tables defined in SQLModel metadata.

    This function should typically be called once at application startup
    to ensure all tables are created.
    """
    logger.info("Initializing database and creating tables (if not exist)")
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialization completed successfully")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    This function is designed to be used with FastAPI's dependency injection
    to ensure that each request has a properly managed session.

    Yields:
        Generator[Session, None, None]: A SQLModel Session instance.
    """
    logger.debug("Creating a new database session")
    with Session(engine) as session:
        try:
            yield session
        finally:
            logger.debug("Closing the database session")
