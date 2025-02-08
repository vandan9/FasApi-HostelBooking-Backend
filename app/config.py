from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_password_sqlalchemey: str
    database_name: str
    database_username: str
    database_port: str
    EMAIL_HOST : str
    EMAIL_PORT :str
    EMAIL_HOST_USER :str
    EMAIL_HOST_PASSWORD :str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings=Settings()