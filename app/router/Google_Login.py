from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import urllib.parse

from sqlalchemy.orm import Session
from models import Employee
from datetime import timedelta

from core.security import (create_access_token, get_google_access_token, get_google_user_info, get_password_hash)
from db.session import get_db
from models.Employees import Employee
from core.config import settings

router = APIRouter()

# 구글 로그인 관련 엔드포인트 ------------------------------------------------------------------------🔽
@router.get("/google/login", summary="구글 로그인 페이지로 이동")
def google_login():
    oauth_params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",  # 선택: Refresh Token 발급용
        "prompt": "consent"        # 선택: 매번 동의 화면을 띄움 (테스트 시 유리)
    }
    
    # 2. URL 안전한 문자열로 자동 인코딩 (공백 -> +, 특수문자 -> %XX)
    query_string = urllib.parse.urlencode(oauth_params)
    
    # 3. 최종 URL 완성
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    
    # 사용자의 브라우저를 구글 창으로 리다이렉트
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback", summary="구글 로그인 콜백 처리")
async def google_callback(code: str, db: Session = Depends(get_db)):
    try:
        # 1. 구글이 준 code를 진짜 Access Token으로 교환 (비동기)
        access_token = await get_google_access_token(code)
        
        # 2. Access Token으로 구글 유저 정보(이메일, 이름) 가져오기 (비동기)
        user_info = await get_google_user_info(access_token)
        email = user_info.get("email")
        name = user_info.get("name")
        
        if not email:
            raise HTTPException(status_code=400, detail="이메일 정보를 가져올 수 없습니다.")
            
        # 3. 우리 DB에 이미 있는 이메일인지 확인
        existing_user = db.query(Employee).filter(Employee.email == email).first()
        
        if not existing_user:
            temp_token = create_access_token(
                data={"sub": email, "is_setup": True}, 
                expires_delta=timedelta(minutes=15)
            )
            # 4-A. [신규 유저] DB에 없으면 자동 회원가입 진행
            
            frontend_setup_url = f"https://localhost/api/v1/auth/social_setup?token={temp_token}&email={email}&name={name}"
            #email과 name을 쿼리 파라미터로 프론트엔드에 전달하여, 추가 정보 입력 페이지에서 사용할 수 있도록 합니다.
            return RedirectResponse(url=frontend_setup_url)
            
        else:
            # 5. 로그인 처리가 완료되었으므로, 우리 서비스 전용 JWT 토큰 생성
            jwt_token = create_access_token(data={"sub": existing_user.email})
        
        # 6. 최종 결과 리턴
        return {"message": "구글 로그인 성공", "access_token": jwt_token, "token_type": "bearer"} # 차후 리다이렉트 URL로 변경 예정
        
    except Exception as e:
        print(f"OAuth Error Detail: {e}")
        raise HTTPException(status_code=500, detail="구글 로그인 처리 중 서버 오류가 발생했습니다.")
    
@router.get("/social_setup", summary="소셜 로그인으로 가입한 유저의 추가 정보 입력 페이지")
def social_signup_setup():
    # 구글 로그인으로 가입한 유저는 비밀번호가 없으므로, 추가 정보 입력 페이지로 리다이렉트
    return RedirectResponse(url="/social-setup")