# this script routes the login request to the login handler
import logging
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from src.appconfig import app_constants
from src.models.login_model import LoginOutput, LoginInput, GuestLoginOutput, GuestLoginInput, SignupOutput, SignupInput
from src.handlers.login_handler import LoginHandler
from src.utils.database_utils import get_db
from src.utils.user_session_manager import UserSessionManager

# routes for the login page and login api.
# instantiate the user session manager singleton to manage user sessions
router = APIRouter()
userSessionManager = UserSessionManager()
logging.basicConfig(level=logging.INFO)


@router.post(app_constants.Login.apiLoginUrl, response_model=LoginOutput)
def login(input: LoginInput, response: Response, db: Session = Depends(get_db)):
    '''
    this event is invoked when the player logs in
    this script routes the login request to the login handler
    
    Args:
        input (LoginInput): the login input model
        response (Response): the response object

    Raises:
        HTTPException: if the user does not exist

    Returns:
        LoginOutput: the login output model
    '''
    try:
        handler = LoginHandler()
        userInfo = handler.checkLogin(input = input, db = db)

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
        
        return LoginOutput(username=userInfo['username'], user_privileges=userInfo['user_privilege'], token='would be too easy man, get outta here')

    except Exception as e:
        print(e)


@router.post(app_constants.Login.apiGuestLoginUrl, response_model=GuestLoginOutput)
def guest_login(input: GuestLoginInput, response: Response):
    '''
    this event is invoked when the player logs in as a guest

    Args:
        input (GuestLoginInput): the guest login input model
        response (Response): the response object

    '''
    
    try:
        handler = LoginHandler()
        userInfo = handler.checkGuestLogin(input = input)

        # if user exists create a new session for the user and return the token. else raise an exception
        if not userInfo:
            raise HTTPException(status_code=400, detail="something went wrong creating the guest user")
        
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
        
        return GuestLoginOutput(username=userInfo['username'], user_privileges=userInfo['user_privilege'], token='would be too easy man, get outta here')
        
    except Exception as e:
        print(e)
        
@router.post(app_constants.Signup.apiSignupUrl, response_model=SignupOutput)
def signup(input: SignupInput, response: Response, db: Session = Depends(get_db)):
    '''
    this event is invoked when the player signs up
    this script routes the signup request to the login handler
    
    Args:
        input (SignupInput): the signup input model
        response (Response): the response object
        
    Returns:
        SignupOutput: the signup output model
    '''
    input.user_privilege = 'player'
    try:
        handler = LoginHandler()
        signup_output = handler.checkSignup(input = input, db = db)

        return signup_output
    
    except Exception as e:
        print(e)