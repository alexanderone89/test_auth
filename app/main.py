from fastapi import FastAPI
from app.users.router import router as router_users
from app.source.router import router as router_sources


app = FastAPI()

app.include_router(router_users)
app.include_router(router_sources)
