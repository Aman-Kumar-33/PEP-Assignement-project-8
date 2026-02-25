from pydantic import BaseModel
from typing import Optional

# --- CATEGORY SCHEMAS ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# --- SERVICE SCHEMAS ---
class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    duration_minutes: int
    category_id: int

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    provider_id: int
    category: CategoryResponse  # Automatically includes the linked category details!

    class Config:
        from_attributes = True