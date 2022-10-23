from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str 
    DB_PASSWORD: str
    DB_NAME: str 
    DB_USERNAME: str 
    secret_key: str 
    algorithm: str 
    MINS_EXPIRE: int 

    class Config:
        env_file = ".env"


sttngs = Settings()