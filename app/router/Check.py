from fastapi import FastAPI, APIRouter

router = APIRouter()
        
@router.get("/check")
async def check():
    return {"message": "Server is running properly", "code" : 200}