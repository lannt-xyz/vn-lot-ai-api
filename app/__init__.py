from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination

# Create a FastAPI instance
app = FastAPI()

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

# Add pagination to the FastAPI application
add_pagination(app)
