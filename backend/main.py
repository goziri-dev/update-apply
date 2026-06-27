from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api.v1.routers.user_router import router as user_router
from infra.database import init_db
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start-up events
    await init_db()
    yield
    # Shut-down events


app = FastAPI(title="UpdateApply", lifespan=lifespan)

app.include_router(user_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.SERVER_HOST, 
        port=settings.SERVER_PORT, 
        reload=False if settings.SERVER_HOST != "127.0.0.1" else True
    )
