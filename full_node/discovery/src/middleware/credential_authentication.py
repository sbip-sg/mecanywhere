from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from aiohttp import ClientSession
from config import Config


class CredentialAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: Config, session: ClientSession):
        super().__init__(app)
        self.config = config
        self.session = session


    def token_check(self, request: Request):
        if "Authorization" in request.headers:
            return True
        return False
    

    async def is_authenticated(self, auth_params):
        verify_credential_url = self.config.get_did_service_verify_credential_url()
        async with self.session.post(verify_credential_url, json={}) as result:
            result_status = result.status
            result_json = await result.json()
            is_verified = result_json["result"]
            return result_status == status.HTTP_200_OK and is_verified


    async def dispatch(self, request: Request, call_next):
        # if not self.token_check(request):
        #     return Response("No token.", status_code=status.HTTP_401_UNAUTHORIZED)
        # auth_params = request.headers["Authorization"]
        # if not await self.is_authenticated(auth_params):
        #     return Response("Authentication failed.", status_code=status.HTTP_401_UNAUTHORIZED)
        response = await call_next(request)
        return response
