# this script is used to handle the login of the user
from sqlalchemy.orm import Session
import json
from fastapi import HTTPException

from src.models.login_model import LoginInput, LoginOutput
from src.auth.token import createUserToken
from src.appconfig.app_constants import UserPrivileges
from src.utils.user_session import UserSession
from src.utils.database_utils import DatabaseUtils

class LoginHandler:
    
    def __init__(self, input: LoginInput, db: Session) -> None:
        self.input = input
        self.db = db

    # check if the user exists in the database and if the password is correct returns the LoginOutput
    def checkLogin(self):

        # create a user database object
        user_db = DatabaseUtils(self.db)

        # get the user data from the database
        user_data = user_db.read_user(self.input.username)

        # user_data is a JSON string, parse it to a dictionary
        user_data_dict = json.loads(user_data)

        # Check if user_data contains an error message
        if 'message' in user_data_dict:
            # No user found with the given username
            raise HTTPException(status_code=404, detail=user_data_dict['message'])
        
        # Check if the password matches
        if user_data_dict['user_password'] != self.input.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        # If the password matches, return the user's data
        return user_data_dict

        # TODO: check if the user exists in the database and collect user_id and privilege

        # TODO: check if the password is correct

        # TODO: create logic for guest users
    
    def createUserSession(self, userInfo: dict):
        user_id = userInfo['user_id']
        username = userInfo['username']
        user_privilege = userInfo['user_privilege']

        # create a user session
        userSession = UserSession(user_id=user_id, user_name=username, user_privilege=user_privilege)
        return userSession