from typing import List, Optional

from sqlmodel import Session, select

from app.models.role import Role


class RoleRepository:
    """
    Repository class for accessing Role data from the database.

    Provides methods to list all roles, and get roles by ID or name.
    """

    def __init__(self, session: Session):
        """
        Initialize RoleRepository with a SQLModel Session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def list_all(self) -> List[Role]:
        """
        Retrieve all Role records from the database.

        Returns:
            List[Role]: List of all roles.
        """
        return list(self.session.exec(select(Role)).all())

    def get_by_id(self, role_id: int) -> Optional[Role]:
        """
        Retrieve a Role by its ID.

        Args:
            role_id (int): The ID of the role.

        Returns:
            Optional[Role]: The Role object if found, otherwise None.
        """
        return self.session.get(Role, role_id)

    def get_by_name(self, role_name: str) -> Optional[Role]:
        """
        Retrieve a Role by its name.

        Args:
            role_name (str): The name of the role.

        Returns:
            Optional[Role]: The Role object if found, otherwise None.
        """
        statement = select(Role).where(Role.name == role_name)
        return self.session.exec(statement).first()
