"""
Defines enumerations for application user roles.

RoleName: String-based role names used for role identification.
RoleID: Integer-based role IDs typically matching database IDs.
"""

from enum import Enum


class RoleName(str, Enum):
    """
    Enum representing the string names of user roles.
    """

    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPPORT = "support"
    USER = "user"
    GUEST = "guest"


class RoleID(int, Enum):
    """
    Enum representing the integer IDs of user roles.
    These usually correspond to database primary key values for roles.
    """

    ADMIN = 1
    MODERATOR = 2
    SUPPORT = 3
    USER = 4
    GUEST = 5
