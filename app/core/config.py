from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    OPENSEARCH_COLLECTION_ENDPOINT: str
    Access_Key:str
    Secret_Access_Key:str
    AUTH_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=None,
        case_sensitive=True
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()