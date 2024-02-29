# Import FastAPI for creating the web application and API
from fastapi import FastAPI

# Import modules from the project structure
from src.infrastructure import healthCheck, cleanResults
from src.domain import configLoader
from src.application import workflow

# Initialize the FastAPI app with metadata about the API
app = FastAPI(
    title="Backend APIs For Walmart Scale Up Project",
    description="This is just a test api",
    version="0.1.0",
    # Uncomment the lines below if you want to customize the docs URL or the
    # OpenAPI spec location
    # docs_url=None,
    # openapi_url="/api/openapi.json"
)

# Call the function to clean results at the start-up of the application.
# This ensures that any previous state or data is cleaned before the
# application starts serving new requests.
cleanResults.clean()

# Include routers from different parts of the application.
# This modular approach helps in organizing different API endpoints and
# functionalities.

# Health check router for checking the status of the backend service
app.include_router(healthCheck.router)

# Configuration loader router for loading and managing configuration settings
app.include_router(configLoader.router)

# Workflow router for managing the main workflow of the application
app.include_router(workflow.router)

# Uncomment the line below if you want to run the workflow when the
# application starts.
# This might be used for initialization tasks or preloading models/data.
workflow.run_multiple_model()
