from fastapi import APIRouter

router = APIRouter()


@router.get("/api/healthCheck")
async def healthCheck() -> bool:
    return True
