from fastapi import Request, status
from fastapi.responses import JSONResponse
from auth.jwt_handler import signJWT
from models.user import Users


class UserController:
    def __init__(self) -> None:
        self.user = Users()

    async def save_user(self, data: dict):
        token = await self.user.saveUser(**data)
        token_str = str(token["access_token"].decode("utf-8"))
        print("TOKEN", token_str)
        return JSONResponse(
            status_code=201,
            content={"access_token": token_str,
                     "code": status.HTTP_201_CREATED,
                     "message": "successfully save"},
        )

    async def login(self, data: dict):
        token = await self.user.loginUser(**data)
        token_str = str(token["access_token"].decode("utf-8"))
        return JSONResponse(
            status_code=201,
            content={"data": token_str,
                     "code": status.HTTP_201_CREATED,
                     "message": "successfully logged in"},
        )


