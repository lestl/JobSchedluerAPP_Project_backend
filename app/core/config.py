from pydantic_settings import BaseSettings, SettingsConfigDict, Field
from functools import lru_cache

class Settings(BaseSettings):
    db_host : str = Field(default="127.0.0.1", alias="DB_URL")
    db_port : str = Field(default="3306", alias="DB_PORT")
    db_name : str = Field(alias="DB_NAME")
    db_user : str = Field(alias="DB_USER")
    db_pass : str = Field(alias="DB_PASSWD")
    db_type : str = Field(default="mysql+pymysql", alias="DB_TYPE")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False # 대소문자 구분 안 함 (선택 사항)
    }

@lru_cache
def get_settings() -> Settings:
    """Provides a cached singleton instance of the settings."""
    return Settings()