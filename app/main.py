from fastapi import FastAPI
from app.api.v1 import rag
from app.api.v1 import health
from app.api.v1 import auth

app = FastAPI(title="RAG API")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(rag.router)
