from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.role import Role


class User(SQLModel, table=True):
    """
    Database model representing a user in the system.

    Attributes:
        id (Optional[int]): Primary key for the user.
        username (str): Unique username, indexed for quick search.
        email (str): Unique user email, indexed and required.
        hashed_password (str): Hashed password for authentication.
        full_name (Optional[str]): Optional full name of the user.
        is_active (bool): Status flag indicating if the user is active.
        role_id (Optional[int]): Foreign key referencing the associated role.
        role (Optional[Role]): Relationship to the Role model, back_populates "users".
    """

    __tablename__ = "users"  # pyright: ignore[reportAssignmentType]

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False, max_length=100)
    email: str = Field(index=True, unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)

    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")

    role: Optional[Role] = Relationship(back_populates="users")
