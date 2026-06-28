from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.user_job_profile_schema import UpdateUserJobProfileRequest
from domain.models.user_job_profile import UserJobProfile
from domain.repositories.base_repository import BaseRepository


class UserProfileRepository(BaseRepository[UserJobProfile, UpdateUserJobProfileRequest]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model_class=UserJobProfile, db=db)

    async def read_by_user_id(self, user_id: str) -> UserJobProfile:
        if not self._db:
            raise self._no_db_set_error
        statement = select(UserJobProfile).where(UserJobProfile.user_id == user_id)  # type: ignore[arg-type]
        result = await self._db.execute(statement)
        instance = result.scalar_one_or_none()
        if not instance:
            raise ValueError(f"No UserJobProfile found for user_id={user_id}")
        return instance

    async def update(self, model: UserJobProfile, payload: UpdateUserJobProfileRequest) -> UserJobProfile:
        if not self._db:
            raise self._no_db_set_error
        update_data = payload.model_dump(exclude_unset=True)

        # Map nested LocationQuery objects to flat model fields
        if "current_location" in update_data and update_data["current_location"] is not None:
            model.current_location_city = update_data["current_location"].city
            model.current_location_country = update_data["current_location"].country
        if "desired_location" in update_data and update_data["desired_location"] is not None:
            model.desired_location_city = update_data["desired_location"].city
            model.desired_location_country = update_data["desired_location"].country

        # Apply scalar fields directly
        for field in (
            "first_name",
            "last_name",
            "current_occupation",
            "desired_occupation",
            "years_of_experience",
            "remote_preference",
            "salary_min",
            "phone_number",
        ):
            if field in update_data:
                setattr(model, field, update_data[field])

        await self._db.flush()
        await self._db.refresh(model)
        return model
