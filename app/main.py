# 라이브러리 임포트
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


#router 임포트
from router.Check import router as check_router
from router.Auth import router as auth_router
from router.Google_Login import router as google_login_router

app = FastAPI(
    title="Job Scheduler AOO API",
    description="API for scheduling and managing jobs",
    version="1.0.0"
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(check_router)
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(google_login_router, prefix="/api/v1/auth")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
