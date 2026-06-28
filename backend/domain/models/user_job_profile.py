from sqlmodel import SQLModel, Field, Relationship, func

from .enums import Occupation, RemotePreference
from .user import User


class UserJobProfile(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    current_occupation: Occupation
    desired_occupation: Occupation
    years_of_experience: int | None = None
    current_location_city: str | None = None
    current_location_country: str | None = None
    desired_location_city: str | None = None
    desired_location_country: str | None = None
    remote_preference: RemotePreference
    salary_min: int | None = None
    phone_number: str | None = None

    # Relationships
    user: User = Relationship(back_populates="profile")