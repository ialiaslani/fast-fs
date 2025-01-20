from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.modules.common.database import get_db
from app.modules.user.models import User
from app.modules.user.schemas import UserResponse
from app.modules.auth.schemas import LoginRequest
from app.modules.common.hashing import verify_password
from app.modules.auth.dependency import create_access_token, verify_cookie

router = APIRouter()


@router.post("/login", response_model=UserResponse)
def login(
        response: Response,
        login_data: LoginRequest,
        db: Session = Depends(get_db)
):
    # Authenticate user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token({"sub": user.email})

    # Set cookie with access token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevent JavaScript access to the cookie
        secure=True,  # Send only over HTTPS (set to False for local testing)
    )
    return user


@router.get("/protected", response_model=UserResponse)
def protected_route(current_user: User = Depends(verify_cookie)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"detail": "Successfully logged out"}
