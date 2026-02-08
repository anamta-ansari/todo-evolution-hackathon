from fastapi import APIRouter

router = APIRouter()

@router.get("/api/test")
async def test_endpoint():
    return {"status": "backend is reachable", "test": "success"}

@router.post("/api/test-echo")
async def test_echo(data: dict):
    return {"echo": data, "status": "received"}