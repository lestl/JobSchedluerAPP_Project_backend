# app/createdb.py

import sys
import os

# [핵심] 현재 파일의 부모의 부모 경로(프로젝트 루트)를 시스템 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 이제 app 패키지를 찾을 수 있으므로, 절대 경로(app.db...)로 임포트합니다.
from app.db.session import engine, Base
# 모델들도 테이블 생성을 위해 임포트 (app.models에 다 모여있다고 가정)
from app.models import Department, ShiftGroup, Employee, DailySchedule, LeaveRequest, Notification, Comment

def create_tables():
    print("데이터베이스 연결 및 테이블 생성 시작...")
    Base.metadata.create_all(bind=engine)
    print("✅ 모든 테이블이 성공적으로 생성되었습니다!")

if __name__ == "__main__":
    create_tables()