from fastapi import FastAPI
from src.infrastructure import healthCheck
from src.domain import configLoader
from src.application import workflow

app = FastAPI(
    title="Backend APIs For Walmart Scale Up Project",
    description="""This is just a test api""",
    version="0.1.0",
    # docs_url=None,
    # openapi_url="/api/openapi.json"
)


app.include_router(healthCheck.router)
app.include_router(configLoader.router)
app.include_router(workflow.router)
workflow.run_multiple_model()
