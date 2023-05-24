from fastapi import FastAPI
from routers.account_router import account_router
from routers.issuer_router import issuer_router

app = FastAPI()
app.include_router(account_router)
app.include_router(issuer_router)
