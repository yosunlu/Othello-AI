from fastapi import WebSocket
import logging

from src.auth.token import verifyUserToken

class PvpGameSessionHandler:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket

    def checkWebsocket(self):
        '''
        Check if the websocket is authenticated
        '''
        try:
            tokenCookie = self.websocket._cookies['token']
            payload = verifyUserToken(tokenCookie)
            user_session_id = payload['user_session_id']
        
        except Exception as e:
            logging.info(e)
            return False
        
        else:
            return user_session_id
       
       
        # if not self.websocket._cookies: 
        #     return False
        
        # # check if the user has a jwt token for authentication
        # tokenCookie = self.websocket._cookies['token']
        # if not tokenCookie:
        #     return False

        # # verify the jwt token
        # try:
        #     payload = verifyUserToken(tokenCookie)
        #     user_session_id = payload['user_session_id']

        # except Exception as e:
        #     # logging.info(e)
        #     self.websocket.close(1000, "Not authenticated")
        #     return False

        # return True