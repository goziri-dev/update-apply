from datetime import datetime

from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    last_signed_in_at: datetime


class CreateUserRequest(UserRequest):
    ...

