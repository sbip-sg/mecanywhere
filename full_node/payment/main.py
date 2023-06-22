from fastapi import FastAPI, Depends
from routers.task_router import task_router
from dependencies import has_ca_access

app = FastAPI()
app.include_router(task_router, dependencies=[Depends(has_ca_access)])
