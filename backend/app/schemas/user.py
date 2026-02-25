from pydantic import BaseModel, EmailStr
from backend.app.models.models import RoleEnum

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum = RoleEnum.user

# Properties required when creating a user (includes password)
class UserCreate(UserBase):
    password: str

# Properties returned to the client (excludes password, includes ID)
class UserResponse(UserBase):
    id: int

    # This tells Pydantic to read data even if it's not a standard dictionary 
    # (i.content., reading directly from our SQLAlchemy database model)
    class Config:
        from_attributes = True