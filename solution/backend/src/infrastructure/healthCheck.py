from fastapi import APIRouter

router = APIRouter()


@router.get("/api/healthCheck", response_model=bool)
async def health_check() -> bool:
    """
    Performs a health check of the application.

    This endpoint is used to verify that the application is running and
    responsive.
    It can be utilized by monitoring tools or during deployment processes 
    to ensure
    the application's health status.

    Returns:
        bool: Always returns True to indicate the application is up and
        running.
    """
    return True
