from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=100, description="Username")
    email: EmailStr = Field(..., description="E-mail of the user")
    full_name: Optional[str] = Field(
        None, max_length=255, description="Complete name of the user"
    )
    is_active: Optional[bool] = Field(
        default=True, description="Status of the user account"
    )
    role_id: Optional[int] = Field(
        default=None, description="ID of the role assigned to the user"
    )


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=6, max_length=128, description="Password for the user account"
    )


class UserRead(UserBase):
    id: int = Field(..., description="Unique identifier of the user")

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)

    model_config = ConfigDict(from_attributes=True)
