from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

class Settings(BaseSettings):
     API_V1_STR: str = "/api/v1"


settings = Settings()
