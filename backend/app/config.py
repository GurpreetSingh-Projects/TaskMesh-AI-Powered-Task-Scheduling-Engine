from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    FILE_HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ASSET_TOKEN_EXPIRY_SECONDS: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PORT: int
    B2_KEY_ID: str
    B2_APPLICATION_KEY: str
    B2_ENDPOINT: str
    B2_BUCKET_NAME: str
    MAX_FILE_SIZE: int
    ALLOWED_CONTENT_TYPES: list[str]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
settings = Settings() #type: ignore