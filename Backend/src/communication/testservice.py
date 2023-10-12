from fastapi import APIRouter

from src.appconfig import app_constants
from src.models.login_model import LoginOutput, LoginInput

router = APIRouter()

@router.get(app_constants.Login.apiLoginUrl, response_model=LoginOutput)
def login(input: LoginInput):
    return LoginOutput(username="this is no real username dummy", user_privileges="admin", token="wut???")