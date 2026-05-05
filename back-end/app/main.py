from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import requests, videos

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS for Flutter Web/Mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the generated videos directory to serve files
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="outputs")

# Include Routers
app.include_router(requests.router, prefix=f"{settings.API_V1_STR}/requests", tags=["requests"])
app.include_router(videos.router, prefix=f"{settings.API_V1_STR}/videos", tags=["videos"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}