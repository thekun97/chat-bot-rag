import jwt
import time
from dotenv import load_dotenv
from config.env import env
load_dotenv()

JWT_SECRET = env("SECRET", "vjscvjsf")
JWT_ALGORITHM = env("ALGORITHM", "HS256")

def token_response(token: str):
    return {
        "access_token": token,
    }

def signJWT(userID: str):
    payload = {
        "user_id": userID,
        "expiry": time.time() + 600

    }
    token = jwt.encode(payload, JWT_SECRET, algorithm= JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm= JWT_ALGORITHM)

        return decode_token if decode_token['expiry']> time.time() else None
    except:
        return {}