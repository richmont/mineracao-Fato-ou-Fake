import os
from dotenv import load_dotenv
load_dotenv()
SQLITE_POSTS_FILENAME = os.getenv("SQLITE_POSTS_FILENAME")
if len(SQLITE_POSTS_FILENAME) == 0 or SQLITE_POSTS_FILENAME == None:
    raise TypeError("Verifique seu arquivo .env, SQLITE_POSTS_FILENAME ausente")
