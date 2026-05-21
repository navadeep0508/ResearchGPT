from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.auth_handler import verify_token
from app.db.database import SessionLocal
from app.db.models import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    
    # Strip accidental double "Bearer" prefix if inputted in Swagger UI
    if token.startswith("Bearer "):
        token = token[7:]

    username = verify_token(token)

    if username is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
    finally:
        db.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User for this token no longer exists. Please log in again."
        )

    return username
