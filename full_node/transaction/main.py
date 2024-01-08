import json
from fastapi import FastAPI, Depends
from routers.task_router import task_router
from routers.history_router import history_router
from dependencies import has_ca_access

app = FastAPI(title="Full Node - Transaction")
app.include_router(task_router, dependencies=[Depends(has_ca_access)])
app.include_router(history_router, dependencies=[Depends(has_ca_access)])

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f)
