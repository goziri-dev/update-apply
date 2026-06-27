from datetime import datetime

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    last_signed_in_at: datetime
    phone_number: str
