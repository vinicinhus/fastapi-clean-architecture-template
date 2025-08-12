from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.v1.routes.auth import get_current_user
from app.core.config import settings
from app.core.logging import logger
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix=settings.API_V1_STR + "/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Create a new user.

    Args:
        user_data (UserCreate): Data required to create a new user.
        session (Session): Database session dependency.
        current_user (User): The authenticated user performing the operation.

    Returns:
        UserRead: The created user object.
    """
    logger.info(
        "User %s is creating a new user with email %s",
        current_user.email,
        user_data.email,
    )
    service = UserService(session, current_user)
    new_user = service.create_user(user_data)
    logger.info("New user created with ID %d", new_user.id)
    return new_user


@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session), _: User = Depends(get_current_user)
) -> List[UserRead]:
    """Retrieve a list of all users.

    Args:
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        List[UserRead]: A list of user objects.
    """
    logger.info("Fetching list of users")
    service = UserService(session)
    users = service.list_users()
    logger.info("Retrieved %d users", len(users))
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> UserRead:
    """Retrieve a user by its ID.

    Args:
        user_id (int): The ID of the user.
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        UserRead: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("Fetching user with ID %d", user_id)
    service = UserService(session)
    user = service.get_user_by_id(user_id)
    if not user:
        logger.warning("User with ID %d not found", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info("User with ID %d successfully retrieved", user_id)
    return user


@router.get("/email/{email}", response_model=UserRead)
def get_user_by_email(
    email: str,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> UserRead:
    """Retrieve a user by their email address.

    Args:
        email (str): The email of the user.
        session (Session): Database session dependency.
        _ (User): The authenticated user (not used directly).

    Returns:
        UserRead: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("Fetching user with email %s", email)
    service = UserService(session)
    user = service.get_user_by_email(email)
    if not user:
        logger.warning("User with email %s not found", email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info("User with email %s successfully retrieved", email)
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Update an existing user's information.

    Args:
        user_id (int): The ID of the user to update.
        user_data (UserUpdate): The updated user data.
        session (Session): Database session dependency.
        current_user (User): The authenticated user performing the operation.

    Returns:
        UserRead: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("User %s is updating user with ID %d", current_user.email, user_id)
    service = UserService(session, current_user)
    updated_user = service.update_user(user_id, user_data)
    if not updated_user:
        logger.warning("User with ID %d not found for update", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info("User with ID %d successfully updated", user_id)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user by its ID.

    Args:
        user_id (int): The ID of the user to delete.
        session (Session): Database session dependency.
        current_user (User): The authenticated user performing the operation.

    Returns:
        None

    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("User %s is deleting user with ID %d", current_user.email, user_id)
    service = UserService(session, current_user)
    if not service.delete_user(user_id):
        logger.warning("User with ID %d not found for deletion", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info("User with ID %d successfully deleted", user_id)
    return None
