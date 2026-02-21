from pwdlib import PasswordHash  # 패스워드 해시 암호화 라이브러리
from datetime import datetime, timedelta, timezone
import httpx
from jose import jwt
from typing import Optional, Dict, Any
from pwdlib import PasswordHash

from core.config import settings


# to get a string like this run:
# openssl rand -hex 32
# OAuth 로직 ------------------------------------------------------------------------🔽
SECRET_KEY = settings.JWT_SECRET_KEY # JWT 토큰을 서명하는 데 사용되는 비밀 키
ALGORITHM = "HS256" # SHA-256 해싱 알고리즘을 사용하여 토큰을 서명하는 데 사용되는 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Access Token Expire time in Minutes

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token" #구글 OAuth 2.0 토큰 엔드포인트 URL
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo" #구글 OAuth 2.0 사용자 정보 엔드포인트 URL

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # timedelta 객체는 시간 간격을 나타내며, expires_delta는 토큰의 만료 시간을 설정
    """사용자 정보를 담은 JWT 토큰을 발행합니다."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # 토큰의 만료 시간을 현재 시간에 expires_delta를 더하여 계산
    else: # expires_delta가 수동적으로 제공되지 않은 경우, 기본적으로 ACCESS_TOKEN_EXPIRE_MINUTES를 사용하여 만료 시간을 설정
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # 비밀키를 사용해 JWT를 암호화하여 생성
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_google_access_token(code: str) -> str:
    """구글이 준 일회용 'code'를 진짜 'Access Token'으로 교환합니다."""
    
    data = { # 구글 토큰 엔드포인트에 POST 요청으로 보내는 데이터 해당 양식 은 구글 OAuth 2.0 문서에 명시된 양식
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code, # 구글이 로그인 성공 후 리다이렉트 URI로 보내주는 일회용 코드
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }
    
    # 비동기 HTTP 요청 (외부 서버 통신 시 서버가 멈추지 않게 async/await 사용)
    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_URL, data=data)
        
        if response.status_code != 200:
            raise ValueError("구글 토큰을 발급받는데 실패했습니다.")
            
        token_data = response.json()
        return token_data.get("access_token")

async def get_google_user_info(access_token: str) -> Dict[str, Any]:
    """구글 Access Token을 이용해 유저의 프로필 정보(이메일, 이름)를 가져옵니다."""
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise ValueError("구글 로그인 유저 정보를 가져오는데 실패했습니다.")
            
        return response.json() # {"email": "...", "name": "...", "picture": "..."} 포함



# 패스워드 해시 로직 ------------------------------------------------------------------------🔽

pwd_context = PasswordHash.recommended()

pwd_context = pwd_context
# bcrypt 알고리즘으로 암호화 deprecated="auto"는 이전 버전의 알고리즘을 자동으로 감지하여 지원하는 옵션입니다.
# CryptContext라는 객체를 생성


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
    # 받은 패스워들르 객체를 통해 해쉬 변환


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    # 받은 암호화된 패스워드를 같은 알고리즘을 사용하여 평문 패스워드와 비교하여 일치 여부를 반환
