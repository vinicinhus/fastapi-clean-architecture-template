from typing import List, Optional

from sqlmodel import Session, select

from app.models.user import User


class UserRepository:
    """
    Repository class for accessing User data from the database.

    Provides methods to create, retrieve, update, list, and delete users.
    """

    def __init__(self, session: Session):
        """
        Initialize UserRepository with a database session.

        Args:
            session (Session): The database session.
        """
        self.session = session

    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        Args:
            user (User): The User instance to be created.

        Returns:
            User: The created User instance with updated state (e.g. id).
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by its ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The User instance if found, else None.
        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email of the user.

        Returns:
            Optional[User]: The User instance if found, else None.
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def list_all(self) -> List[User]:
        """
        Retrieve all users from the database.

        Returns:
            List[User]: List of all User instances.
        """
        statement = select(User)
        return list(self.session.exec(statement).all())

    def update(self, user: User, updated_data: dict) -> User:
        """
        Update a user's attributes and save changes to the database.

        Args:
            user (User): The existing User instance to update.
            updated_data (dict): A dictionary of attributes to update.

        Returns:
            User: The updated User instance.
        """
        for key, value in updated_data.items():
            setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by its ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user was found and deleted, False otherwise.
        """
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
