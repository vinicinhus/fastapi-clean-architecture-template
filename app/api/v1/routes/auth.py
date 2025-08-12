from datetime import timedelta
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.config import settings
from app.core.logging import logger
from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.session import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix=settings.API_V1_STR + "/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Dict[str, str]:
    """Authenticate a user and generate an access token.

    This endpoint validates the provided username and password. If the credentials
    are correct, it generates and returns a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Login form data containing username and password.
        session (Session): Database session dependency.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.
    """
    logger.info("Login attempt for username: %s", form_data.username)
    repo = UserRepository(session)
    user = repo.get_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(
            "Login failed: Incorrect password for username or user not found %s",
            form_data.username,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info("User %s successfully logged in", form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    """Retrieve the currently authenticated user from the token.

    Decodes the provided JWT token to extract the user ID, then fetches
    the corresponding user from the database.

    Args:
        token (str): The JWT token provided in the Authorization header.
        session (Session): Database session dependency.

    Returns:
        User: The authenticated user object.
    """
    logger.debug("Decoding access token for current user retrieval")
    payload = decode_access_token(token)
    if not payload:
        logger.error("Token decoding failed or token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = payload.get("sub")
    if sub is None:
        logger.error("Token payload is missing the subject (sub)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = int(sub)
    logger.debug("Fetching user with ID %d from database", user_id)
    user = session.get(User, user_id)
    if not user:
        logger.error("User with ID %d not found", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("Current user successfully retrieved: %s", user.email)
    return user
