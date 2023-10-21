# user session manager to handle user sessions

import uuid
import logging
from fastapi import WebSocket, WebSocketDisconnect, Depends
from src.handlers.login_handler import LoginHandler
from typing import Dict, List, Optional, Union
from src.auth.token import createUserToken

# TODO: handle logout to clear user session manager

logging.basicConfig(level=logging.INFO)

class UserSessionManager:

    def __init__(self) -> None:
        # stores all the active user sessions in the server holding user_id, username, and privilege
        self.sessions: Dict[str, Dict[str, Union[str, int]]] = {}

    
    # connect a user to the server adding the user to the sessions dictionary and gives a token to the user
    def connect(self, userInput: dict):
        user_id = userInput['user_id']
        username = userInput['username']
        user_privilege = userInput['user_privilege']

        # generate a random uuid sessionID for the user and serialize it
        sessionId = str(uuid.uuid4())

        # add the user to the sessions dictionary
        self.sessions[sessionId] = {
            'user_id': user_id,
            'username': username,
            'user_privilege': user_privilege,
        }

        # logging the user session info
        logging.info(f"Session ID: {sessionId}")
        logging.info(f"User ID: {user_id}")
        logging.info(f"Username: {username}")
        logging.info(f"User Privilege: {user_privilege}")

        # create a token for the user
        token = createUserToken(user_id=user_id, username=username, user_privilege=user_privilege)
        userInput['token'] = token

        return