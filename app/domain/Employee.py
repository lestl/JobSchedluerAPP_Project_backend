from pydantic import BaseModel
from typing import Optional
from datetime import date


class Employee_signup(BaseModel): # 회원가입 스키마 정의
    name: str
    email: str
    password: str  # 입력은 그냥 패스워드
    department_id: Optional[int] = None  # Optional로 설정하여 선택적으로 입력할 수 있도록 함
    shift_group_id: Optional[int] = None
    rank: str
    role: str = "USER"
    birth_date: date
