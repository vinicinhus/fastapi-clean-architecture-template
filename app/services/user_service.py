from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.logging import logger
from app.core.security import get_password_hash
from app.enums.role import RoleID, RoleName
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate


class UserService:
    """
    Service layer for user-related business logic.

    Handles user creation, retrieval, updating, and deletion,
    including role validation and permission checks.
    """

    def __init__(self, session: Session, current_user: Optional[User] = None):
        """
        Initialize UserService with database session and optionally current authenticated user.

        Args:
            session (Session): Database session to be used.
            current_user (Optional[User]): The currently authenticated user.
        """
        self.user_repository = UserRepository(session)
        self.role_repository = RoleRepository(session)
        self.current_user = current_user

    def _validate_user_role(self, role_id: Optional[int]):
        """
        Validate that a role with the given ID exists.

        Args:
            role_id (Optional[int]): Role ID to validate.

        Raises:
            HTTPException: If the role does not exist.
        """
        if role_id is None:
            logger.debug("No role_id provided for validation, skipping.")
            return

        logger.debug("Validating role with ID %s", role_id)
        role = self.role_repository.get_by_id(role_id)
        if not role:
            logger.warning("Role validation failed: role ID %s does not exist", role_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with ID {role_id} does not exist.",
            )
        logger.debug("Role with ID %s validated successfully", role_id)

    def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Create a new user with the provided data.

        Only users with admin role can create new users.

        Args:
            user_data (UserCreate): Data for creating a new user.

        Returns:
            UserRead: The created user data.

        Raises:
            HTTPException: If the current user lacks permission or role is invalid.
        """
        if (
            not self.current_user
            or not self.current_user.role
            or self.current_user.role.name != RoleName.ADMIN
        ):
            logger.warning(
                "Permission denied: User %s tried to create a user without admin role",
                getattr(self.current_user, "email", "Anonymous"),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can create users.",
            )

        role_id = user_data.role_id or RoleID.GUEST.value

        self._validate_user_role(role_id)

        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role_id=user_data.role_id,
        )
        created_user = self.user_repository.create(user)
        return UserRead.model_validate(created_user)

    def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The user's email.

        Returns:
            Optional[UserRead]: The user data if found, else None.
        """
        user = self.user_repository.get_by_id(user_id)
        return UserRead.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The user's email.

        Returns:
            Optional[UserRead]: The user data if found, else None.
        """
        user = self.user_repository.get_by_email(email)
        return UserRead.model_validate(user) if user else None

    def list_users(self) -> List[UserRead]:
        """
        Retrieve all users.

        Returns:
            List[UserRead]: List of all users.
        """
        users = self.user_repository.list_all()
        return [UserRead.model_validate(user) for user in users]

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserRead]:
        """
        Update an existing user with provided data.

        Admins can update any user; regular users can only update their own data.

        Args:
            user_id (int): The ID of the user to update.
            user_data (UserUpdate): Data to update the user with.

        Returns:
            Optional[UserRead]: The updated user data if user exists, else None.

        Raises:
            HTTPException: If the current user lacks permission or role is invalid.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        if not self.current_user or (
            self.current_user.role.name
            != RoleName.ADMIN  # pyright: ignore[reportOptionalMemberAccess]
            and self.current_user.id != user_id
        ):  # pyright: ignore[reportOptionalMemberAccess]
            logger.warning(
                "Permission denied: User %s tried to update user ID %d",
                getattr(self.current_user, "email", "Anonymous"),
                user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this user.",
            )

        updated_data = user_data.model_dump(exclude_unset=True)

        if "role_id" not in updated_data or updated_data["role_id"] is None:
            updated_data["role_id"] = user.role_id
        else:
            self._validate_user_role(updated_data["role_id"])

        # If password is provided, hash it before updating
        if "password" in updated_data and updated_data["password"]:
            updated_data["hashed_password"] = get_password_hash(
                updated_data.pop("password")
            )

        updated_user = self.user_repository.update(user, updated_data)
        return UserRead.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Admins can delete any user; regular users can only delete their own account.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if user was deleted, False otherwise.

        Raises:
            HTTPException: If the current user lacks permission.
        """
        if not self.current_user or (
            self.current_user.role.name
            != RoleName.ADMIN  # pyright: ignore[reportOptionalMemberAccess]
            and self.current_user.id != user_id
        ):  # pyright: ignore[reportOptionalMemberAccess]
            logger.warning(
                "Permission denied: User %s tried to delete user ID %d",
                getattr(self.current_user, "email", "Anonymous"),
                user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this user.",
            )
        return self.user_repository.delete(user_id)
