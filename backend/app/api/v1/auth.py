from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.crud import crud_user
from backend.app.core import security

router = APIRouter()

@router.post("/login")
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Log in to get a JWT access token. 
    Note: OAuth2 expects 'username', so pass your email into the username field.
    """
    # 1. Find user by email (form_data.username contains the email from the login form)
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    # 2. Verify user exists and password is correct
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Define token expiration time
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 4. Create the JWT token containing the user's ID
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # 5. Return the token in the exact format Swagger UI expects
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }