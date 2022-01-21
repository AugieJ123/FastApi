from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # For development purpose
        # env_file = "../.env"

        # for alembic migration and prodution
        env_file = ".env"

settings = Settings()