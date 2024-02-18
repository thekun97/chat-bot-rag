from pydantic import BaseModel, Field, validator
from auth.jwt_handler import signJWT, decodeJWT
from db.repository import Repository
from fastapi import HTTPException


class Users(Repository):
    # async def index(self, add):
    #     await add([('', "")])

    def collection(self):
        return 'user'

    async def saveUser(self, name: str, password: str):
        data = {"name": name,
                "password": password}
        user = await self.getUser(name)
        print(user)
        if (user):
            raise HTTPException(status_code=500, detail="User Already Exists. Login instead")
        user = await self.save(data=data, collection_name=self.collection())
        if (user):
            return signJWT(name)
        else:
            return []

    async def loginUser(self, name: str, password: str):
        user = await self.getUser(name)
        print(user)
        if (user):
            if (user[0]["password"] == password):
                return signJWT(name)
            else:
                raise HTTPException(status_code=403, detail="Invalid password or Email")
        else:
            raise HTTPException(status_code=403, detail="Invalid password or Email")

    async def getUser(self, name: str):
        result = await self.find({"name": name}, self.collection())
        return result
