from enum import Enum
import json
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError
from datetime import datetime, timedelta
from config import Config
from aiohttp import ClientSession
from models.credential import CredentialModel
import redis


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
class CredentialAuthenticationMiddleware:
    def __init__(self, config: Config, session: ClientSession, redis: redis.Redis):
        self.config = config
        self.session = session
        self.redis = redis

    async def _verify_vc(self, did: str, vc: dict):
        verifiedDID = self.redis.get(json.dumps(vc))
        if verifiedDID is not None:
            return verifiedDID == did

        async with self.session.post(
            self.config.get_verify_vc_url(), json=vc
        ) as result:
            result_status = result.status
            result_json = await result.json()
            is_result_true = "result" in result_json and result_json["result"]
            is_verified = (
                result_status == status.HTTP_200_OK
                and is_result_true
                and did == vc["credential"]["claim"]["DID"]
            )
            if is_verified:
                self.redis.set(json.dumps(vc), did)
            return is_verified

    def check_expiry(self, expiry: float):
        if datetime.fromtimestamp(expiry) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired.",
                headers={"WWW-Authenticate": "Bearer"},
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

            self.check_expiry(payload["exp"])

            vc = {"credential": payload["credential"]}
            did = payload["did"]
            return await self._verify_vc(did, vc)

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
            self.check_expiry(payload["exp"])
            vc = {"credential": payload["credential"]}
            did = payload["did"]
            if await self._verify_vc(did, vc):
                return CredentialAuthenticationMiddleware._create_token(
                    did, vc, TokenType.ACCESS
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
