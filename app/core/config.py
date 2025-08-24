from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_file_size: int = 5 * 1024 * 1024
    upload_dir: str = "app/output"
    allowed_extensions: set = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    class Config:
        env_file = ".env"

settings = Settings()