from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import router as api_router
from app.core.config_service import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI backend for apartment management and customer service chatbot",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # This is now a property that returns a list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    from app.core.config_service import config_service

    # Get host and port from configuration
    host = config_service.get("host", "0.0.0.0")
    port = config_service.get("port", 9000)

    uvicorn.run(app, host=host, port=port)