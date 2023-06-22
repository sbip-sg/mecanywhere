from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.login_service import LoginService
from dependencies import get_login_service

login_router = APIRouter(dependencies=[Depends(get_login_service)])

@login_router.post("/create_challenge/")
async def create_challenge(
    request: Request, 
    login_service: LoginService = Depends(get_login_service)
):
    data = await request.json()
    # did = data['did']
    challenge = login_service.create_challenge()
    return challenge

@login_router.post("/verify_response/")
async def verify_response(
    request: Request, 
    login_service: LoginService = Depends(get_login_service)
):
    data = await request.json()
    message = data['message']
    publicKey = data['publicKey']
    signature = data['signature']
    is_authenticated = login_service.verify_response(message, signature, publicKey)
    return is_authenticated

# @login_router.post("/verify_response/")
# async def verify_response(
#     request: Request, 
#     login_service: LoginService = Depends(get_login_service)
# ):
#     data = await request.json()
#     did = data['did']
#     signedChallenge = data['signedChallenge']
#     challenge = data['challenge']
#     print("signedChallenge", signedChallenge)
#     is_authenticated = login_service.verify_response(did, signedChallenge, challenge)
#     print("is_authenticated", is_authenticated)
#     return is_authenticated