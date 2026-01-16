from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # MongoDB
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.environ.get('DB_NAME', 'email_scheduler_db')
    
    # Redis
    REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Ethereal Email SMTP
    ETHEREAL_SMTP_HOST: str = os.environ.get('ETHEREAL_SMTP_HOST', 'smtp.ethereal.email')
    ETHEREAL_SMTP_PORT: int = int(os.environ.get('ETHEREAL_SMTP_PORT', '587'))
    ETHEREAL_SMTP_USER: str = os.environ.get('ETHEREAL_SMTP_USER', '')
    ETHEREAL_SMTP_PASSWORD: str = os.environ.get('ETHEREAL_SMTP_PASSWORD', '')
    
    # Rate Limiting
    DEFAULT_EMAILS_PER_HOUR: int = int(os.environ.get('DEFAULT_EMAILS_PER_HOUR', '100'))
    DEFAULT_DELAY_SECONDS: int = int(os.environ.get('DEFAULT_DELAY_SECONDS', '2'))
    
    # Worker Concurrency
    CELERY_WORKER_CONCURRENCY: int = int(os.environ.get('CELERY_WORKER_CONCURRENCY', '4'))
    
    # CORS
    CORS_ORIGINS: str = os.environ.get('CORS_ORIGINS', '*')
    
    class Config:
        case_sensitive = True

settings = Settings()
