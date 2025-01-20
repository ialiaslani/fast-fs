from fastapi import FastAPI
from app.api.V1.user import UserRouter
app = FastAPI()

app.include_router(UserRouter.router, prefix="/api/v1/users", tags=["Users"])

