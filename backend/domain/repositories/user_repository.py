from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User
from domain.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, BaseModel]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model_class=User, db=db)

    async def update(self, model: User, payload: BaseModel) -> User:
        if not self._db:
            raise self._no_db_set_error
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(model, field, value)
        await self._db.flush()
        await self._db.refresh(model)
        return model
