from pydantic import BaseModel

class UserSession(BaseModel):
        user_id: str
        user_name: str
        user_privileges: str
        user_email: str = None
        user_token: str