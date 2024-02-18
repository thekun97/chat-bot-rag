from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if (credentials):
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid credentials")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid credentials")

    def verify_token(token: str):
        isValidToken = False
        verified = decodeJWT(token)
        if verified:
            isValidToken = True
        return isValidToken