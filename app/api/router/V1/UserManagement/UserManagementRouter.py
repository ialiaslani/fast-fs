from idlelib.query import Query

from fastapi import APIRouter

from app.core.application.features.UserManagment.Queries.GetUserListQueryHandler import GetUserListQueryHandler

UserManagementRouter = APIRouter()


@UserManagementRouter.get('/users')
async def get_users(query: str | None = None):
    operation = GetUserListQueryHandler(query)
    operation_result = await operation.GetUserListQueryResult(query)
    return operation_result
