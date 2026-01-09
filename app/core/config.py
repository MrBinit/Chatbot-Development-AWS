from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str
    S3_BUCKET: str
    LOCAL_PDF_DIR: str
    EMBEDDING_MODEL_ID: str

    class Config:
        env_file= ".env"

settings = Settings()
