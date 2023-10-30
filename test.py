from dotenv import load_dotenv
from pathlib import Path
import os

# envPath = Path('.') / 'Backend' / '.conf' / '.env'
# load_dotenv(dotenv_path=envPath)

# TOKEN_KEY = os.getenv('TOKEN_KEY')
# ALGORITHM = os.getenv('ALGORITHM')

userInfo = {
    "playerusername": ["sessionid"]
}

userSessions = {}
session_id = "1234"

key = next(iter(userInfo))
if next(iter(userInfo)) not in userSessions:
    userSessions[next(iter(userInfo))] = []
userSessions[next(iter(userInfo))].append(session_id)


print(userSessions)