from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str

class LoginOutput(BaseModel):
    username: str
    user_privileges: str
    token: str