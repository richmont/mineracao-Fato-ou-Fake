import os
from dotenv import load_dotenv
load_dotenv()
SQLITE_POSTS_FILENAME = os.getenv("SQLITE_POSTS_FILENAME")
SQLITE_TOKENS_FILENAME = os.getenv("SQLITE_TOKENS_FILENAME")
if len(SQLITE_POSTS_FILENAME) == 0 or SQLITE_POSTS_FILENAME == None:
    raise TypeError("Verifique seu arquivo .env, SQLITE_POSTS_FILENAME ausente")
if len(SQLITE_TOKENS_FILENAME) == 0 or SQLITE_TOKENS_FILENAME == None:
    raise TypeError("Verifique seu arquivo .env, SQLITE_TOKENS_FILENAME ausente")