from fastapi import FastAPI

from app.api.router.V1.UserManagement.UserManagementRouter import UserManagementRouter

app = FastAPI()

app.include_router(UserManagementRouter)