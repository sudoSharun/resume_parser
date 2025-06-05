from fastapi import FastAPI, Depends
from app.endpoints import routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

app = FastAPI(
    title="RESUME PARSER",
    description="This API accepts resume and extract important details from it",
    version="1.0",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(routes.router, tags=["RESUME PARSER"])

@app.get("/healthcheck", tags=["Default"])
async def healthcheck() -> dict:
    """
    Health check endpoint.
    Returns status code and message to indicate the service is running.
    """
    return {"status_code": 200, "message": "Service is running"}

@app.get("/", tags=["Default"])
async def root() -> dict:
    """
    Root endpoint.
    Returns the title, description and version of the API.
    """
    return {"title": app.title, "description": app.description, "version": app.version}