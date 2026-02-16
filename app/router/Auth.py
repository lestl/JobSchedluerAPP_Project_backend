from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from domain.Employee import Employee_signup
from core.security import get_password_hash
from models import Employee

router = APIRouter()

def check_registered_user(email: str, db: Session):
    # 사용자 등록 여부 확인 로직 구현 ------------------------------------🔽

    existing_user = db.query(Employee).filter(
        Employee.email == email).first()

    # 사용자 이메일 존재 여부 확인

    if existing_user:
        return False  # 이미 등록된 사용자
    return True  # 등록되지 않은 사용자


@router.post("/api/v1/auth/signup", status_code=status.HTTP_201_CREATED)
def register_user(user: Employee_signup, db: Session = Depends(get_db)):
    # 사용자 등록 로직 구현 ------------------------------------🔽
    exist = check_registered_user(user.email, db)
    # 사용자 존재 여부 확인
    if not exist:
        raise HTTPException(status_code=400,
                            detail="이미 등록된 이메일입니다.")
        # FastAPI에서는 HTTPException을 사용하여 HTTP 오류 응답을 생성
        # 기존의 그냥 리턴은 flask에서 사용되던 방식

    # 사용자 비밀번호 해싱 ------------------------------------🔽
    hashed_password = get_password_hash(user.password)
    print("DEBUG : ", hashed_password, "LEN", len(hashed_password))
    # 사용자 등록 처리 로직 구현 ------------------------------------🔽
    new_user = Employee(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        rank=user.rank,
        birth_date=user.birth_date,
        department_id=user.department_id,
        shift_group_id=None  # ShiftGroup은 관리자가 나중에 지정할 수 있도록 None으로 초기화
    )

    # db에 사용자 정보 저장, 비밀번호 해싱 등 ---------------------🔽
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="사용자 등록 중 오류가 발생했습니다.")

    return {"message": "회원가입 완료되었습니다.", "email": new_user.email, "name": new_user.name}
