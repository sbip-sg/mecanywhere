from fastapi import FastAPI
from routers.account_router import account_router

app = FastAPI()
app.include_router(account_router)
