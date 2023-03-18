from pydantic import BaseSettings

class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()