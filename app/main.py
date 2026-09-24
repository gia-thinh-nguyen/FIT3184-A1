from fastapi import FastAPI
from a2wsgi import WSGIMiddleware
from app.routers import core, ops
from app.dashboard import dash_app

app = FastAPI()
app.include_router(core.router)
app.include_router(ops.router)

app.mount("/dashboard", WSGIMiddleware(dash_app.server))