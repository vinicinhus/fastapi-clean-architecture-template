from typing import List, Optional

from sqlmodel import Session

from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleRead


class RoleService:
    """
    Service layer for role-related business logic.

    This class interacts with the RoleRepository to retrieve role data,
    and converts ORM models to Pydantic schema models.
    """

    def __init__(self, session: Session):
        """
        Initialize the RoleService with a database session.

        Args:
            session (Session): The database session to be used by the repository.
        """
        self.repository = RoleRepository(session)

    def list_roles(self) -> List[RoleRead]:
        """
        Retrieve all roles and convert them to RoleRead schemas.

        Returns:
            List[RoleRead]: List of roles as schema instances.
        """
        roles = self.repository.list_all()
        return [RoleRead.model_validate(role) for role in roles]

    def get_role_by_id(self, role_id: int) -> Optional[RoleRead]:
        """
        Retrieve a role by its ID and convert it to a RoleRead schema.

        Args:
            role_id (int): The ID of the role.

        Returns:
            Optional[RoleRead]: The role as a schema instance if found, else None.
        """
        role = self.repository.get_by_id(role_id)
        return RoleRead.model_validate(role) if role else None

    def get_role_by_name(self, role_name: str) -> Optional[RoleRead]:
        """
        Retrieve a role by its name and convert it to a RoleRead schema.

        Args:
            role_name (str): The name of the role.

        Returns:
            Optional[RoleRead]: The role as a schema instance if found, else None.
        """
        role = self.repository.get_by_name(role_name)
        return RoleRead.model_validate(role) if role else None
