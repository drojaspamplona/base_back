from pydantic import Field, validator
from pydantic_settings import BaseSettings
from typing import Optional

class BaseSettingModel(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "allow"

class DbConfig(BaseSettingModel):
    host: str = Field(..., alias='HOST')
    user: str = Field(..., alias='USER')
    password: str = Field(..., alias='PASSWORD')
    dbname: str = Field(..., alias='DBNAME')

class JwtConfig(BaseSettingModel):
    secret_key: str = Field(..., alias='SECRET_KEY')
    algorithm: str = Field(..., alias='ALGORITHM')
    access_token_subject: str = "access"
    expire_time: int = 15


class SmtpConfig(BaseSettingModel):
    host: str = "smtp.gmail.com"
    ssl: bool = True
    port: int = 465
    user: str = Field(..., alias='SMTP_USER')
    password: str = Field(..., alias='SMTP_PASSWORD')


class RedisConfig(BaseSettingModel):
    host: str = Field(..., alias='REDIS_HOST')
    port: int = 6379
    ssl: bool = False
    db: int = 0


class Settings(BaseSettingModel):
    environment: str = Field(..., alias='ENVIRONMENT')
    project_name: str = Field(..., alias='PROJECT_NAME')
    api_url: str = "/api"
    docs_url: Optional[str] = "/docs"
    salt_secret: str = Field(..., alias='SALT_SECRET')
    db_config: DbConfig = DbConfig()
    jwt_config: JwtConfig = JwtConfig()
    smtp: SmtpConfig = SmtpConfig()
    redis_config: RedisConfig = RedisConfig()
    allowed_origin: str = Field(..., alias='ALLOWED_ORIGIN')

settings = Settings()
