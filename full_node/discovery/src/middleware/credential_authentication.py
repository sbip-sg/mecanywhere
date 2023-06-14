from enum import Enum
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError
from datetime import datetime, timedelta
from config import Config
from aiohttp import ClientSession
from models.did import DIDModel
from models.credential import CredentialModel
from starlette.middleware.base import BaseHTTPMiddleware


ALGORITHM = "HS256"
ACCESS_SECRET_KEY = "secret"
REFRESH_SECRET_KEY = "secretsecret"
ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES = 15
REFRESH_TOKEN_DEFAULT_EXPIRE_MINUTES = 60 * 24  # 1 day

security = HTTPBearer()


class TokenType(Enum):
    ACCESS = 1
    REFRESH = 2


# Custom middleware authenticating credentials in authorization header,
# does not override dispatch to allow docs to render.
# Credential refers to HTTP Authorization header with Bearer token.
# VC refers to Verifiable Credential.
class CredentialAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: Config, session: ClientSession):
        super().__init__(app)
        self.config = config
        self.session = session

    async def _verify_vc(self, did: str, vc: dict):
        async with self.session.post(
            self.config.get_verify_vc_url(), json=vc
        ) as result:
            result_status = result.status
            result_json = await result.json()
            is_verified = "result" in result_json and result_json["result"]
            return (
                result_status == status.HTTP_200_OK
                and is_verified
                and did == vc["credential"]["claim"]["DID"]
            )

    # Returns true if the token is valid and the vc is verified
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
                key=ACCESS_SECRET_KEY,
                algorithms=[ALGORITHM],
            )
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            vc = {"credential": payload["credential"]}
            return await self._verify_vc(payload["did"], vc)

        except JOSEError as e:  # catches any exception
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Creates a token with the given subject and expiration time
    def _create_token(
        did: str, vc: dict, type: TokenType, expires_delta: timedelta | None = None
    ):
        if type == TokenType.ACCESS:
            default_expires = ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES
            typed_secret_key = ACCESS_SECRET_KEY
        else:
            default_expires = REFRESH_TOKEN_DEFAULT_EXPIRE_MINUTES
            typed_secret_key = REFRESH_SECRET_KEY
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=default_expires)
        to_encode = vc.copy()
        to_encode.update({"did": did, "exp": expire})
        encoded_jwt = jwt.encode(to_encode, typed_secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    # Creates a token with the given did and expiration time after verifying the vc
    async def verify_and_create_tokens(
        self,
        did: str,
        vc: CredentialModel,
        access_expires_delta: timedelta | None = None,
        refresh_expires_delta: timedelta | None = None,
    ):
        if await self._verify_vc(did, vc):
            return (
                CredentialAuthenticationMiddleware._create_token(
                    did, vc, TokenType.ACCESS, access_expires_delta
                ),
                CredentialAuthenticationMiddleware._create_token(
                    did, vc, TokenType.REFRESH, refresh_expires_delta
                ),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Verifiable Credential.",
            )

    async def refresh_access(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token,
                key=REFRESH_SECRET_KEY,
                algorithms=[ALGORITHM],
            )
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            vc = {"credential": payload["credential"]}
            if await self._verify_vc(payload["did"], vc):
                return CredentialAuthenticationMiddleware._create_token(
                    payload["did"], vc, TokenType.ACCESS
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid Verifiable Credential.",
                )

        except JOSEError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )
