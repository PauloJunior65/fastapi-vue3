from pydantic import BaseSettings

class Settings(BaseSettings):
    ADMIN_EMAIL="deadpool@example.com"
    APP_NAME="ChimichangApp"
    
    class Config:
        env_file = ".env"

# global instance
settings = Settings()