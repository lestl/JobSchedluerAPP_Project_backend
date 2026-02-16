# 라이브러리 임포트
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# DB 모델 임포트
from db.session import get_db
from models import Employee, Department, ShiftGroup, DailySchedule, LeaveRequest, Notification, Comment

#router 임포트
from router.Check import router as check_router
from router.Auth import router as auth_router

app = FastAPI(
    title="Job Scheduler AOO API",
    description="API for scheduling and managing jobs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(check_router)
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
