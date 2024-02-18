from dotenv import load_dotenv
from config.env import env

load_dotenv()


def db() -> dict:
    return {
        "db": {
            "url": env("MONGO_URL", "mongodb://localhost:27017/"),
            "name":  env("MONGO_DBNAME", "database_name"),
            "user": env("MONGO_USER", ""),
            "password": env("MONGO_PASS", "")
        }
    }
