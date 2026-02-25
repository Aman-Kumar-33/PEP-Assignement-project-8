from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import service as service_schema

# --- CATEGORY DATABASE LOGIC ---

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of all categories."""
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: service_schema.CategoryCreate):
    """Create a new category (like 'Haircare' or 'Consulting')."""
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# --- SERVICE DATABASE LOGIC ---

def get_services(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of all services, available to the public."""
    return db.query(models.Service).offset(skip).limit(limit).all()

def get_service_by_id(db: Session, service_id: int):
    """Fetch a single service by its ID."""
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def create_service(db: Session, service: service_schema.ServiceCreate, provider_id: int):
    """
    Create a new service. 
    Notice we pass `provider_id` separately from the service data!
    """
    db_service = models.Service(
        title=service.title,
        description=service.description,
        price=service.price,
        duration_minutes=service.duration_minutes,
        category_id=service.category_id,
        provider_id=provider_id  # Automatically assigned from the logged-in user!
    )
    
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service