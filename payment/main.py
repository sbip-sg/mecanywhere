from fastapi import FastAPI, Depends
from routers.payment_router import payment_router
from dependencies import has_ca_access

app = FastAPI(title="Cloud - Payment")
app.include_router(payment_router, dependencies=[Depends(has_ca_access)])
