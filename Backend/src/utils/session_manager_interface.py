# this script is used to define the interface for the session managers

from abc import ABC, abstractmethod
from typing import Optional
from src.models.user_session_model import UserSessionModel
from src.models.game_session_model import GameSessionModel

class SessionManagerInterface(ABC):

    @abstractmethod
    def connect(self) -> None:
        '''
        connect a user session or a game session to the respective session manager
        '''
        pass

    @abstractmethod
    def disconnect(self) -> None:
        '''
        disconnect a user session ot a game session from the respective session manager
        '''
        pass