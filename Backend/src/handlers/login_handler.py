# this script is used to handle the login of the user
from src.models.login_model import LoginInput, LoginOutput
from src.auth.token import createUserToken
from src.appconfig.app_constants import UserPrivileges

class LoginHandler:
    
    def __init__(self, input: LoginInput) -> None:
        # TODO: initialize the database
        self.input = input

    # check if the user exists in the database and if the password is correct returns the LoginOutput
    def checkLogin(self):
        # Get the user input
        username = self.input.username
        password = self.input.password
        user_id = self.input.user_id

        # TODO: check if the user exists in the database and collect user_id and privilege

        # TODO: check if the password is correct

        # TODO: create logic for guest users

        userInfo = {
            'user_id': user_id,
            'username': username,
            'user_privilege': UserPrivileges.player,
        }
        return userInfo