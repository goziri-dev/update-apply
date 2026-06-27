from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User
from domain.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model_class=User, db=db)
