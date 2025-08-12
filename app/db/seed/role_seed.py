from sqlmodel import Session, select

from app.core.logging import logger
from app.enums.role import RoleName
from app.models.role import Role


def init_roles(session: Session) -> None:
    """
    Initialize default roles in the database.

    Iterates through all roles defined in the RoleName enum and ensures that
    each one exists in the database. If a role is missing, it is created.

    Args:
        session (Session): The active SQLModel database session.

    Returns:
        None
    """
    created_count = 0

    for role_enum in RoleName:
        logger.debug("Checking if role '%s' exists", role_enum.value)
        role_exists = session.exec(select(Role).where(Role.name == role_enum)).first()
        if not role_exists:
            logger.info("Creating missing role '%s'", role_enum.value)
            session.add(Role(name=role_enum))
            created_count += 1

    session.commit()
    logger.info("Role initialization completed. %d new roles created.", created_count)
