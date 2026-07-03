from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(
    title="Workflow Agent AI Backend",
    description="Backend API for the AI Workflow Agent project.",
    version="0.1.0",
)

app.include_router(router)



