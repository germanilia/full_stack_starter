from pydantic_settings import BaseSettings
from typing import Optional, List, Union


class Settings(BaseSettings):
    """
    Application settings that loads from environment variables
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "My Boilerplate App"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database settings
    DATABASE_URL: Optional[str] = None
    DB_NAME: str = "mydatabase"
    
    # Security settings
    SECRET_KEY: str = "your_secret_key"
    
    # Application settings
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    ALLOWED_HOSTS: Union[str, List[str]] = ["localhost", "127.0.0.1"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def model_post_init(self, __context):
        """Process values after initialization"""
        # Convert ALLOWED_HOSTS from comma-separated string to list if it's a string
        if isinstance(self.ALLOWED_HOSTS, str):
            self.ALLOWED_HOSTS = [host.strip() for host in self.ALLOWED_HOSTS.split(",")]


settings = Settings()