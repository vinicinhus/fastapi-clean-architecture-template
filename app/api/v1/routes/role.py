from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.v1.routes.auth import get_current_user
from app.core.config import settings
from app.core.logging import logger
from app.db.session import get_session
from app.models.user import User
from app.schemas.role import RoleRead
from app.services.role_service import RoleService

router = APIRouter(prefix=settings.API_V1_STR + "/roles", tags=["Roles"])


@router.get("/", response_model=List[RoleRead])
def list_roles(
    session: Session = Depends(get_session), _: User = Depends(get_current_user)
) -> List[RoleRead]:
    """Retrieve a list of all available roles.

    Args:
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        List[RoleRead]: A list of role objects.
    """
    logger.info("Fetching list of roles")
    service = RoleService(session)
    roles = service.list_roles()
    logger.info("Retrieved %d roles", len(roles))
    return roles


@router.get("/{role_id}", response_model=RoleRead)
def get_role_by_id(
    role_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> RoleRead:
    """Retrieve a role by its ID.

    Args:
        role_id (int): The ID of the role.
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        RoleRead: The role object if found.

    Raises:
        HTTPException: If the role is not found.
    """
    logger.info("Fetching role with ID %d", role_id)
    service = RoleService(session)
    role = service.get_role_by_id(role_id)
    if not role:
        logger.warning("Role with ID %d not found", role_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    logger.info("Role with ID %d successfully retrieved", role_id)
    return role


@router.get("/name/{role_name}", response_model=RoleRead)
def get_role_by_name(
    role_name: str,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> RoleRead:
    """Retrieve a role by its name.

    Args:
        role_name (str): The name of the role.
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        RoleRead: The role object if found.

    Raises:
        HTTPException: If the role is not found.
    """
    logger.info("Fetching role with name '%s'", role_name)
    service = RoleService(session)
    role = service.get_role_by_name(role_name)
    if not role:
        logger.warning("Role with name '%s' not found", role_name)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    logger.info("Role with name '%s' successfully retrieved", role_name)
    return role
