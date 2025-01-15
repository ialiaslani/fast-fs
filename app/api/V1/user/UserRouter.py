from fastapi import APIRouter
from app.modules.user.models import UserRead,UserCreate
from app.core import database

router = APIRouter()

@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate):
    # Data validation
    if not user.email or not user.password:
        raise ValueError("Email and password are required.")

    # Check if the user already exists
    existing_user = database.fetch_one("SELECT * FROM users WHERE email = :email", {"email": user.email})
    if existing_user:
        raise ValueError("User already exists.")

    # Create a new user in the database
    new_user_id = database.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {
        "email": user.email,
        "password": user.password
    })

    # Get new user details
    new_user = database.fetch_one("SELECT * FROM users WHERE id = :id", {"id": new_user_id})

    return new_user
