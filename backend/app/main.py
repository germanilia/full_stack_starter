from fastapi import FastAPI
import logging
import os
from app.routers import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))