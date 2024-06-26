# this script is used to generate and decode tokens for users
import datetime
import os
import jwt

from jwt import encode, decode
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
# from src.appconfig.app_constants import UserPrivileges

#  TODO: validate user_id in the token payload using authentication dependency injection
#  TODO: if times permits handle token expiration and refresh

# envPath = Path('.') / 'Backend' / '.conf' / '.env'
# load_dotenv(dotenv_path=envPath)

TOKEN_KEY = os.getenv('TOKEN_KEY')
ALGORITHM = os.getenv('ALGORITHM')
# TOKEN_EXPIRATION = os.getenv('TOKEN_EXPIRATION')


# create a token for the user given a valid user_id and return it as a jwt token
def createUserToken(user_session_id: str,
                    user_id: int, 
                    username: Optional[str] = None,
                    user_email: Optional[str] = None, 
                    user_privilege: Optional[str] = 'player') -> str:
                    # user_privilege: Optional[str] = UserPrivileges.player) -> str:
    # info to store in the token
    payload = {
        'user_session_id': user_session_id,
    }

    # if user_id, user_email, username or user_privilege are provided, add them to the payload
    if user_id:
        payload['user_id'] = user_id
    if username:
        payload['username'] = username
    if user_email:
        payload['user_email'] = user_email
    if user_privilege:
        payload['user_privilege'] = user_privilege

    token = encode(payload, TOKEN_KEY, algorithm=ALGORITHM)
    return token


# verify the token and return the payload
def verifyUserToken(token: str) -> dict:
    try:
        payload = decode(token, TOKEN_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        print(e)
        return None
    
if __name__ == "__main__":

    # TOKEN_KEY = "CAPTAIN DUCK"
    # ALGORITHM = "HS256"
    # TOKEN_EXPIRATION = 60 * 30 # 30 minutes

    token = createUserToken(user_id=1, username="test", user_email="nah", user_privilege='player')
    print(token)
    payload = verifyUserToken(token)
    print(payload)

