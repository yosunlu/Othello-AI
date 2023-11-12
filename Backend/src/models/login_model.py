from pydantic import BaseModel
from typing import Optional

class LoginInput(BaseModel):
    username: str
    password: str
    user_id: Optional[str] = None

class LoginOutput(BaseModel):
    username: str
    user_privileges: str
    token: str

class GuestLoginInput(BaseModel):
    username: str

class GuestLoginOutput(BaseModel):
    username: str
    user_privileges: str
    token: str