from pydantic import BaseModel, Field

from domain.models.enums import Occupation, RemotePreference


class LocationQuery(BaseModel):
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=2, max_length=2, pattern=r"^[A-Z]{2}$")


class UserJobProfileRequest(BaseModel):
    user_id: str
    current_location: LocationQuery
    desired_location: LocationQuery
    current_occupation: Occupation
    desired_occupation: Occupation
    years_of_experience: int | None
    remote_preference: RemotePreference
    salary_min: int | None = None
    phone_number: str | None = None
