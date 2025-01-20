from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.modules.common.database import get_db
from app.modules.common.hashing import hash_password
from app.modules.user.models import User
from app.modules.user.schemas import UserCreate, UserResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/all", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Fetch all users
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Fetch a specific user by ID
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the existing user fields
    db_user.name = user.name
    db_user.email = user.email
    db_user.hashed_password = hash_password(user.password)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)  # Refresh the instance with the latest DB state
    return db_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Fetch the user instance by ID
    db_user = db.query(User).get(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user instance
    db.delete(db_user)

    # Commit the transaction
    db.commit()

    # Return the deleted user details (optional)
    return db_user

