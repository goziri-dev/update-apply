from typing import Optional

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    last_signed_in_at: datetime

    # Relationships
    profile: Optional["UserJobProfile"] = Relationship(back_populates="user")  # type: ignore[valid-type]
