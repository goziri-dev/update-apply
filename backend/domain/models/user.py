from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    last_signed_in_at: datetime
    phone_number: str
