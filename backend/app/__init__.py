from fastapi import FastAPI
from .routers import example_router  # Import your routers here

app = FastAPI()

# Include routers
app.include_router(example_router)  # Replace with your actual router names

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}