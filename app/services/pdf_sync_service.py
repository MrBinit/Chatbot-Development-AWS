import os

from app.core.logger import get_logger
from app.core.config_loader import load_app_config
from app.infra.s3_bucket import S3Storage
from app.schemas.pdf import PdfSyncResult

logger = get_logger(__name__)

# Load once (cached)
app_config = load_app_config()

AWS_REGION = app_config["aws"]["region"]
S3_BUCKET = app_config["storage"]["s3_bucket"]
LOCAL_PDF_DIR = app_config["storage"]["local_pdf_dir"]


def sync_local_pdfs() -> PdfSyncResult:
    logger.info("Starting local PDF sync job")

    storage = S3Storage(
        bucket_name=S3_BUCKET,
        region=AWS_REGION,
    )

    storage.ensure_bucket_exists()
    storage.enable_versioning()

    uploaded = []

    for filename in os.listdir(LOCAL_PDF_DIR):
        if not filename.endswith(".pdf"):
            continue

        local_path = os.path.join(LOCAL_PDF_DIR, filename)
        s3_key = f"pdfs/{filename}"

        storage.upload_pdf(local_path, s3_key)
        uploaded.append(s3_key)

    return PdfSyncResult(uploaded_files=uploaded)
