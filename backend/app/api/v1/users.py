from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas import user as user_schema
from backend.app.crud import crud_user
from backend.app.db.database import get_db

router = APIRouter()

@router.post("/register", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (Admin, Provider, or Customer).
    """
    # 1. Check if the email is already in use
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # 2. If email is unique, create the user
    return crud_user.create_user(db=db, user=user)