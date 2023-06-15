from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers.account_creation_router import account_creation_router
from routers.login_router import login_router
from routers.registration_router import registration_router
from routers.assignment_router import assignment_router
from routers.monitoring_router import monitoring_router
from dependencies import has_ca_access


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.include_router(registration_router)
app.include_router(account_creation_router)
app.include_router(login_router)
app.include_router(assignment_router, dependencies=[Depends(has_ca_access)])
app.include_router(monitoring_router, dependencies=[Depends(has_ca_access)])


@app.on_event("startup")
async def start_up():
    pass 
