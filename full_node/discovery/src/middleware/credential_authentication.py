from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError
from datetime import datetime, timedelta
from config import Config
from aiohttp import ClientSession
from starlette.middleware.base import BaseHTTPMiddleware


SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES = 15

security = HTTPBearer()


# custom middleware authenticating credentials in authorization header, 
# does not override dispatch to allow docs to render
class CredentialAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: Config, session: ClientSession):
        super().__init__(app)
        self.config = config
        self.session = session


    async def has_access(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        token = credentials.credentials
        print("token => ", token)

        try:
            payload = jwt.decode(
                token,
                key=SECRET_KEY,
                algorithms=[ALGORITHM],
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                    "verify_iss": False,
                },
            )
            print("payload => ", payload)

            verify_credential_url = self.config.get_verify_credential_url()
            async with self.session.post(verify_credential_url, json={}) as result:
                result_status = result.status
                result_json = await result.json()
                is_verified = result_json["result"]
                return True  # result_status == status.HTTP_200_OK and is_verified

        except JOSEError as e:  # catches any exception
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
