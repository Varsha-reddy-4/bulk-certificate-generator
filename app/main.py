from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes.jobs import router as jobs_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating certificates in bulk",
    version="1.0.0"
)


app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }