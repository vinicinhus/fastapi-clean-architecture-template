from pydantic import BaseModel, ConfigDict

from app.enums.role import RoleName


class RoleRead(BaseModel):
    id: int
    name: RoleName

    model_config = ConfigDict(from_attributes=True)
