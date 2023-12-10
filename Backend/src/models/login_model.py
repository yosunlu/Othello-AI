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

class SignupInput(BaseModel):
    username: str
    password: str
    user_privilege: Optional[str] = "player"
    email: str

class SignupOutput(BaseModel):
    username: str
    user_privileges: str
    message: str