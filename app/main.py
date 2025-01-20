from fastapi import FastAPI

from app.api.V1.auth import AuthRouter
from app.api.V1.user import UserRouter
from app.modules.common.elastic import configure_logger

# Configure logger
logger = configure_logger()


app = FastAPI()

app.include_router(UserRouter.router, prefix="/api/v1/users", tags=["Users"])

app.include_router(AuthRouter.router, prefix="/api/v1/auth", tags=["Auth"])

