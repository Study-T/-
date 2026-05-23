from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "root"
    db_name: str = "digitalhuman"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    redis_url: str = "redis://localhost:6379/0"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    s3_bucket: str = "digital-human"

    jwt_secret: str = "change-me-in-production"
    jwt_expire_minutes: int = 10080

    lhm_api_url: str = "http://localhost:8001"
    fashn_api_url: str = "http://localhost:8002"

    sms_provider: str = "aliyun"
    sms_access_key: str = ""
    sms_secret_key: str = ""
    sms_sign_name: str = ""
    sms_template_code: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
