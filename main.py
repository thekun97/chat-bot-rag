from fastapi import FastAPI
from pydantic import BaseModel
from config.env import env
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import user

load_dotenv()


class MetaData(BaseModel):
    partner: str


app = FastAPI()

app.include_router(user.router, tags=['User'], prefix='/api/user')

origins = [
    env("CLIENT_ORIGIN", ""),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def index():
    return {"message": "Health Check !"}
