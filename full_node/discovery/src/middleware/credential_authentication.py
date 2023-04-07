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


# Custom middleware authenticating credentials in authorization header,
# does not override dispatch to allow docs to render.
# Credential refers to HTTP Authorization header with Bearer token.
# VC refers to Verifiable Credential.
class CredentialAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: Config, session: ClientSession):
        super().__init__(app)
        self.config = config
        self.session = session

    async def verify_vc(self, credential: dict):
        async with self.session.post(
            self.config.get_verify_vc_url(), json=credential
        ) as result:
            result_status = result.status
            result_json = await result.json()
            is_verified = result_json["result"]
            return result_status == status.HTTP_200_OK and is_verified

    # Returns true if the token is valid and the credential is verified
    async def has_access(
        self, authorization: HTTPAuthorizationCredentials = Depends(security)
    ):
        if not (authorization and authorization.scheme == "Bearer"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme.",
            )

        token = authorization.credentials

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
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
                )
            return await self.verify_vc(payload)

        except JOSEError as e:  # catches any exception
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # Creates a token with the given data and expiration time
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

    # Creates a token with the given vc and expiration time
    async def verify_and_create_vc_access_token(
        self, credential: dict, expires_delta: timedelta | None = None
    ):
        if await self.verify_vc(credential):
            return CredentialAuthenticationMiddleware.create_access_token(
                credential, expires_delta
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Verifiable Credential.",
            )
