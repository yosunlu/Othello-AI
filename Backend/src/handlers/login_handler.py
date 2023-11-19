# this script is used to handle the login of the user
import uuid
import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.login_model import LoginInput, LoginOutput, GuestLoginInput, GuestLoginOutput
from src.auth.token import createUserToken
from src.appconfig.app_constants import UserPrivileges
from src.utils.user_session import UserSession
from src.utils.database_utils import DatabaseUtils

class LoginHandler:
    
    def __init__(self) -> None:
        pass

    def checkLogin(self, input: LoginInput, db: Session = None):
        '''
        this event is invoked when the player logs in
        check if the user exists in the database and if the password is correct returns the LoginOutput
        
        Args:
            input (LoginInput): the login input model
            db (Session): the database session
            
        Raises:
            HTTPException: if the user does not exist

        Returns:
            userInfo (dict): the user information

        '''
        # create a user database object
        user_db = DatabaseUtils(db)

        # get the user data from the database
        user_data = user_db.read_user(input.username)

        # user_data is a JSON string, parse it to a dictionary
        user_data_dict = json.loads(user_data)

        # Check if user_data contains an error message
        if 'message' in user_data_dict:
            # No user found with the given username
            raise HTTPException(status_code=404, detail=user_data_dict['message'])
        
        # Check if the password matches
        if user_data_dict['user_password'] != input.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        # If the password matches, return the user's data
        return user_data_dict

        # TODO: check if the user exists in the database and collect user_id and privilege

        # TODO: check if the password is correct

        # TODO: create logic for guest users
    
    def checkGuestLogin(self, input: GuestLoginInput):
        '''
        this event is invoked when the player logs in as a guest
        creates a new user with a passed username and assigns a uuid to that user
        
        Args:
            input (GuestLoginInput): the guest login input model

        Returns:
            userSession (UserSession): the user session object
        '''

        # create a unique id for the guest user
        guest_user_id = str(uuid.uuid4())

        # create a user data dictionary
        userInfo = {
            'user_id': guest_user_id,
            'username': input.username,
            'user_privilege': UserPrivileges.player
        }

        return userInfo
    
    def checkSignup(self, input: LoginInput, db: Session = None):
        '''
        this event is invoked when the player signs up
        creates a new user with a passed username password and privilege into the database
        
        Args:
            input (LoginInput): the signup input model
        '''
        

    def createUserSession(self, userInfo: dict):
        user_id = userInfo['user_id']
        username = userInfo['username']
        user_privilege = userInfo['user_privilege']

        # create a user session
        userSession = UserSession(user_id=user_id, user_name=username, user_privilege=user_privilege)
        return userSession