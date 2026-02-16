from passlib.context import CryptContext  # 패스워드 해시 암호화 라이브러리

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context = pwd_context
# bcrypt 알고리즘으로 암호화 deprecated="auto"는 이전 버전의 알고리즘을 자동으로 감지하여 지원하는 옵션입니다.
# CryptContext라는 객체를 생성


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
    # 받은 패스워들르 객체를 통해 해쉬 변환


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    # 받은 암호화된 패스워드를 같은 알고리즘을 사용하여 평문 패스워드와 비교하여 일치 여부를 반환
