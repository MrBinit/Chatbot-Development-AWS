from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENSEARCH_COLLECTION_ENDPOINT: str
    Access_Key:str
    Secret_Access_Key:str
    
    class Config:
        env_file= ".env"

settings = Settings()
