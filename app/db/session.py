from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus  # [추가] URL 인코딩용 라이브러리

# 설정 불러오기
try:
    from app.core.config import settings
except ImportError:
    from app.core import settings

# [핵심 해결책]
# 비밀번호에 '@', '#', ':' 같은 특수문자가 섞여있으면 SQLAlchemy가 주소를 잘못 해석합니다.
# quote_plus로 감싸주면 이를 안전한 문자열(%40, %23 등)로 변환해줍니다.
encoded_password = quote_plus(settings.DB_PASSWORD)
encoded_user = quote_plus(settings.DB_USER)

# 변환된 비밀번호를 사용해 URL 생성
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{encoded_user}:{encoded_password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,   # 실행되는 쿼리 로그 출력
    pool_pre_ping=True, # 연결 끊김 시 자동 재연결
    connect_args={"charset": "utf8mb4"}
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 정의
Base = declarative_base()

# 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()