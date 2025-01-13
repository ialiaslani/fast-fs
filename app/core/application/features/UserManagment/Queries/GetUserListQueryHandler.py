from app.core.domain.UserManagement import User


class GetUserListQueryHandler:
    def __init__(self, repositories):
        self.repositories = repositories

    async def GetUserListQueryResult(self, query):
        repository = self.repositories.get(User)
        result = await repository.get(query)
        return result