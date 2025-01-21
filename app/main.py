from fastapi import FastAPI
from app.api.V1.auth import AuthRouter
from app.api.V1.user import UserRouter
from app.middlewares.request_logger import RequestLoggerMiddleware

app = FastAPI()

app.add_middleware(RequestLoggerMiddleware)


app.include_router(UserRouter.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(AuthRouter.router, prefix="/api/v1/auth", tags=["Auth"])
