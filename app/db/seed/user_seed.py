from sqlmodel import Session, select

from app.core.config import settings
from app.core.logging import logger
from app.core.security import get_password_hash
from app.models.user import User


def init_admin_user(session: Session) -> None:
    """
    Initialize the admin user if it does not already exist.

    Checks if a user with the configured ADMIN_USER username exists.
    If not found, creates a new admin user with default settings.

    Args:
        session (Session): The active SQLModel database session.

    Returns:
        None
    """
    logger.debug("Checking if admin user '%s' exists", settings.ADMIN_USER)
    admin_user = session.exec(
        select(User).where(User.username == settings.ADMIN_USER)
    ).first()

    if admin_user:
        logger.info(
            "Admin user '%s' already exists (ID: %d)",
            admin_user.username,
            admin_user.id,
        )
        return

    logger.info(
        "Creating admin user '%s' with email '%s'",
        settings.ADMIN_USER,
        settings.ADMIN_EMAIL,
    )
    new_admin_user = User(
        username=settings.ADMIN_USER,
        email=settings.ADMIN_EMAIL,
        full_name=settings.ADMIN_FULL_NAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        is_active=True,
        role_id=1,  # role_id=1 is admin role
    )
    session.add(new_admin_user)
    session.commit()
    session.refresh(new_admin_user)
    logger.info(
        "Admin user '%s' created successfully with ID %d",
        new_admin_user.username,
        new_admin_user.id,
    )
