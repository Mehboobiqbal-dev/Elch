from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.config import settings
from core.db import SessionLocal
import models

# This OAuth2 scheme is used by FastAPI to extract the token from the request.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """
    Dependency function to get a database session for a request.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            # Suppress DB close/rollback exceptions (e.g., aborted connections) to avoid cascading 500s
            import logging
            logging.error(f"DB session close failed: {e}")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Decodes the JWT token from the request, validates it, and retrieves the user from the database.
    This is a synchronous function and is used as a dependency in API endpoints.
    It MUST be `def`, not `async def`.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Synchronously decode the JWT token
        payload = jwt.decode(token, settings.SESSION_SECRET, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Synchronously query the database for the user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user