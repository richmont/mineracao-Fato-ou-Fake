import os
from dotenv import load_dotenv
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
if len(MONGO_URL) == 0 or MONGO_URL is None:
    raise TypeError("Verifique seu arquivo .env, MONGO_URL ausente")