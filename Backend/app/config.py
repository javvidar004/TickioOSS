from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://tickio_user:tickio_pass@db:5432/tickio_db"
    SECRET_KEY: str = "changeme-super-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"


settings = Settings()
