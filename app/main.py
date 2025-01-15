from fastapi import FastAPI
from api.V1.user import UserRouter
app = FastAPI()

app.include_router(UserRouter)

