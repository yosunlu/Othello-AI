# this script routes the login request to the login handler
import logging
from fastapi import APIRouter, HTTPException, Response

from src.appconfig import app_constants
from src.models.login_model import LoginOutput, LoginInput
from src.handlers.login_handler import LoginHandler
from src.utils.user_session_manager import UserSessionManager

# routes for the login page and login api.
# instantiate the user session manager singleton to manage user sessions
router = APIRouter()
userSessionManager = UserSessionManager()
logging.basicConfig(level=logging.INFO)


@router.post(app_constants.Login.apiLoginUrl, response_model=LoginOutput)
def login(input: LoginInput, response: Response):
    '''
    this event is invoked when the player logs in
    this script routes the login request to the login handler
    
    Args:
        input (LoginInput): the login input model
        response (Response): the response object

    Raises:
        HTTPException: if the user does not exist
    '''
    try:
        handler = LoginHandler(input)
        userInfo = handler.checkLogin()

        # if user exists create a new session for the user and return the token. else raise an exception
        if not userInfo:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        userSession = handler.createUserSession(userInfo)
        
        # connect the user session to the user session manager and creates a token for the user
        userSessionManager.connect(userSession)
        
        # set the token in the cookie
        response.set_cookie(
            key="token", 
            value=userSession.getUserToken(),
            httponly=True,
            secure = False,
            samesite="lax"
            )

    except Exception as e:
        print(e)

    return LoginOutput(username=userInfo['username'], user_privileges=userInfo['user_privilege'], token='would be too easy man, get outta here')