from pydantic import BaseModel
from typing import Optional
from datetime import date


# class Employee_signup(BaseModel): # 회원가입 스키마 정의
#     name: str
#     email: str
#     password: str  # 입력은 그냥 패스워드
#     check_password: str  # 패스워드 확인 필드 추가
#     department_id: Optional[int] = None  # Optional로 설정하여 선택적으로 입력할 수 있도록 함
#     shift_group_id: Optional[int] = None
#     rank: str
#     role: str = "USER"
#     birth_date: date

class Employee_social_signup(BaseModel): # 소셜 로그인 회원가입 스키마 정의
    temp_token: str        # 아까 발급해준 임시 토큰
    name : str                # 소셜 로그인 시 이름도 받아야 DB에 저장 가능
    department_id: Optional[int] = None
    shift_group_id: Optional[int] = None
    rank: str = "사원"
    role: str = "USER"
    birth_date: date
    