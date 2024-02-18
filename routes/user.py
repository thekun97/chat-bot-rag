from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from controllers.user_controller import UserController

router = APIRouter()


class Register(BaseModel):
    name: str
    password: str


UserController = UserController()


@router.post('/sign-up')
async def sign_up(credentials: Register):
    response = await UserController.save_user(credentials.model_dump())
    return response


@router.post('/login')
async def sign_up(credentials: Register):
    response = await UserController.login(credentials.model_dump())
    return response
