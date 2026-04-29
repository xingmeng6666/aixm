from fastapi import FastAPI
from api.routes import router
from db.database import engine, Base

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Multi-Agent Automation Platform",
    description="API for managing and orchestrating multiple agents.",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Agent Platform API"}
