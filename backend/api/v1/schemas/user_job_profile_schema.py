from pydantic import BaseModel, Field, field_validator

from domain.models.enums import Occupation, RemotePreference


class LocationQuery(BaseModel):
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=2, max_length=2, pattern=r"^[A-Z]{2}$")


class UserJobProfileRequest(BaseModel):
    current_location: LocationQuery
    desired_location: LocationQuery
    current_occupation: Occupation
    desired_occupation: Occupation
    years_of_experience: int | None
    remote_preference: RemotePreference
    salary_min: int | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @field_validator("desired_occupation")
    @classmethod
    def validate_desired_occupation_is_not_student(cls, value: Occupation) -> Occupation:
        if value == Occupation.STUDENT:
            raise ValueError("Desired occupation cannot be 'student'")
        return value


class UpdateUserJobProfileRequest(BaseModel):
    current_location: LocationQuery | None = None
    desired_location: LocationQuery | None = None
    current_occupation: Occupation | None = None
    desired_occupation: Occupation | None = None
    years_of_experience: int | None = None
    remote_preference: RemotePreference | None = None
    salary_min: int | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @field_validator("desired_occupation")
    @classmethod
    def validate_desired_occupation_is_not_student(cls, value: Occupation) -> Occupation:
        if value is not None and value.value == "student":
            raise ValueError("Desired occupation cannot be 'student'")
        return value
