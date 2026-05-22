from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.api_title)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(api_router)
