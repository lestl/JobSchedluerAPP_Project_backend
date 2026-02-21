from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Employee
import secrets
from jose import JWTError, jwt

# DB, Domain
from db.session import get_db
from domain.Employee import Employee_social_signup

#core
from core.security import create_access_token, get_google_access_token, get_password_hash
from core.config import settings

router = APIRouter()

SECRET_KEY = settings.JWT_SECRET_KEY # JWT 토큰을 서명하는 데 사용되는 비밀 키
ALGORITHM = "HS256" # SHA-256 해싱 알고리즘을 사용하여 토큰을 서명하는 데 사용되는 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Access Token Expire time in Minutes

def check_registered_user_verify(email: str, db: Session):
    # 사용자 등록 여부 확인 로직 구현 ------------------------------------🔽

    existing_user = db.query(Employee).filter(Employee.email == email).first()
    # 사용자 이메일 존재 여부 확인

    if existing_user:
        return False  # 이미 등록된 사용자
    return True  # 등록되지 않은 사용자

def check_password_verify(password: str, check_password: str):
    # 비밀번호 검증 로직 구현 ------------------------------------🔽
    if password != check_password:
        return False  # 비밀번호와 확인 비밀번호가 일치하지 않음
    
    return password == check_password  # 1차 비밀번호 회원가입 시 검증


@router.post("/social-signup", status_code=status.HTTP_201_CREATED)
def finalize_social_signup(request: Employee_social_signup, db: Session = Depends(get_db)):
    """추가 정보를 받아 소셜 로그인을 최종 완료하고 DB에 저장합니다."""
    
    try:
        # 1. 임시 토큰 해독해서 이메일 꺼내기 (조작된 토큰인지 검증)
        payload = jwt.decode(request.temp_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        is_setup = payload.get("is_setup")
        
        if email is None or not is_setup:
            raise HTTPException(status_code=401, detail="유효하지 않은 가입 토큰입니다.")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었거나 변조되었습니다. 다시 구글 로그인을 시도해주세요.")

    # 2. 이미 중간에 가입해버렸는지 한 번 더 체크 (방어 로직)
    if not check_registered_user_verify(email, db):
        raise HTTPException(status_code=400, detail="이미 가입이 완료된 계정입니다.")

    # 3. 구글 유저용 더미 비밀번호 생성
    dummy_password = f"social_{secrets.token_urlsafe(16)}"
    hashed_pw = get_password_hash(dummy_password)

    # 4. DB에 최종 저장 (프론트에서 넘겨준 부서, 직급 정보 포함)
    new_user = Employee(
        name=request.name, # 이름도 폼에서 다시 받거나, 토큰에 넣어서 가져올 수 있습니다.
        email=email,
        password=hashed_pw,
        role="USER",
        rank=request.rank,
        birth_date=request.birth_date,
        department_id=request.department_id,
        shift_group_id=request.shift_group_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 5. 최종 가입 완료되었으니 진짜 로그인 토큰 발급
    jwt_token = create_access_token(data={"sub": new_user.email})

    return {
        "message": "회원가입 및 로그인이 완료되었습니다.", 
        "access_token": jwt_token,
        "token_type": "bearer"
    }

