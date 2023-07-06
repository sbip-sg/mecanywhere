from fastapi import FastAPI
from routers.private_router import private_router
from routers.public_router import public_router

app = FastAPI(title="PO - Authentication")
app.include_router(private_router)
app.include_router(public_router)
