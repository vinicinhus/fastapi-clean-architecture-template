from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.enums.role import RoleName

if TYPE_CHECKING:
    from app.models.user import User  # Avoid circular import issues


class Role(SQLModel, table=True):
    """
    Database model for user roles.

    Attributes:
        id (Optional[int]): Primary key of the role.
        name (RoleName): Unique name of the role, indexed for fast lookup.
        users (List[User]): List of users assigned to this role.

    Notes:
        The `users` attribute defines a one-to-many relationship with the User model,
        using `back_populates` to enable bidirectional access.
    """

    __tablename__ = "roles"  # pyright: ignore[reportAssignmentType]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: RoleName = Field(index=True, unique=True, description="Role name")

    users: List["User"] = Relationship(back_populates="role")
