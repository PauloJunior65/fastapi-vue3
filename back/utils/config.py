from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST="127.0.0.1"
    REDIS_PORT=6379
    REDIS_PASSWORD=""
    REDIS_DB=1
    
    class Config:
        env_file = ".env"

# global instance
settings = Settings()