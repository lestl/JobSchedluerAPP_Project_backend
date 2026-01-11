from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # config.py에서 생성한 settings 인스턴스 임포트

st = settings()


# DB 엔진 생성
engine = create_engine(f"{st.db_type}://{st.db_user}:{st.db_pass}@{st.db_host}:{st.db_port}/{st.db_name}")
# mysql+pymysql://user:password@host:port/database 형식

# 세션 생성 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성 주입을 위한 함수 (필요 시) it may do the closing the db server
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()