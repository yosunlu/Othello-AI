from dotenv import load_dotenv
from pathlib import Path
import os

envPath = Path('.') / 'Backend' / '.conf' / '.env'
load_dotenv(dotenv_path=envPath)

TOKEN_KEY = os.getenv('TOKEN_KEY')
ALGORITHM = os.getenv('ALGORITHM')

pass