from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import user as user_schema
from backend.app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    # 1. Hash the password
    hashed_password = get_password_hash(user.password)
    
    # 2. Create the SQLAlchemy model instance
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    
    # 3. Add to database and save
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Refresh to get the generated ID
    
    return db_user