from functools import wraps
from fastapi import HTTPException, Request, status, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.modules.auth.dependency import SECRET_KEY, ALGORITHM
from app.modules.common.database import get_db
from app.modules.user.models import User


def authenticate_with_cookie():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, db: Session = Depends(get_db), **kwargs):
            # Extract the token from the cookie
            token = request.cookies.get("access_token")
            if not token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            try:
                # Decode the token and extract user information
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                email = payload.get("sub")
                if email is None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            # Query the database for the user
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            # Inject the authenticated user into the route
            return await func(*args, request, db, **kwargs)

        return wrapper
    return decorator
