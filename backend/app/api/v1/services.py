from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas import service as service_schema
from backend.app.crud import crud_service
from backend.app.db.database import get_db
from backend.app.api.deps import get_current_user
from backend.app.models import models

router = APIRouter()

# --- CATEGORY ENDPOINTS ---

@router.get("/categories", response_model=List[service_schema.CategoryResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Public endpoint: Anyone can view categories."""
    return crud_service.get_categories(db, skip=skip, limit=limit)

@router.post("/categories", response_model=service_schema.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: service_schema.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Requires a valid JWT token!
):
    """Create a new category. Must be logged in."""
    # Note: In a fully fleshed out app, you'd likely restrict this to 'admin' users only.
    return crud_service.create_category(db=db, category=category)


# --- SERVICE ENDPOINTS ---

@router.get("/", response_model=List[service_schema.ServiceResponse])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Public endpoint: Anyone can view available services."""
    return crud_service.get_services(db, skip=skip, limit=limit)

@router.post("/", response_model=service_schema.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service: service_schema.ServiceCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Requires a valid JWT token!
):
    """
    Create a new service. 
    Role-Based Access Control: Only 'provider' or 'admin' roles can do this.
    """
    # 1. Check if the logged-in user has the right permissions
    if current_user.role.value not in ["provider", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to create services."
        )
    
    # 2. If they are a provider, create the service and attach their user ID!
    return crud_service.create_service(db=db, service=service, provider_id=current_user.id)