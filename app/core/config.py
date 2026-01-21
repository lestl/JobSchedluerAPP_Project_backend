from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # session.py와 변수명을 맞추기 위해 대문자로 정의합니다.
    # alias는 .env 파일에 적힌 키 값(변수명)입니다.
    
    DB_HOST: str = Field("127.0.0.1", alias="DB_HOST")  # .env의 DB_HOST 값을 읽어 DB_HOST에 저장
    DB_PORT: int = Field(3306, alias="DB_PORT")
    DB_NAME: str = Field("shift_db", alias="DB_NAME")
    DB_USER: str = Field("root", alias="DB_USER")
    DB_PASSWORD: str = Field("password", alias="DB_PASSWD") # .env엔 DB_PASSWD, 코드에선 DB_PASSWORD

    # Pydantic V2 설정 방식
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # .env에 정의되지 않은 값이 있어도 에러 내지 않음
    )

# [핵심] 여기서 클래스를 실행해 객체를 만들어야 'import settings'가 작동합니다.
settings = Settings()