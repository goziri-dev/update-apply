from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user_job_profile import UserJobProfile
from domain.repositories.base_repository import BaseRepository


class UserProfileRepository(BaseRepository[UserJobProfile]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model_class=UserJobProfile, db=db)
