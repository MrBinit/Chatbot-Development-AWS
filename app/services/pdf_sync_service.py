import os
from app.core.logger import get_logger
from app.core.config import settings
from app.infra.s3_bucket import S3Storage
from app.schemas.pdf import PdfSyncResult

logger = get_logger(__name__)


def sync_local_pdfs() -> PdfSyncResult:
    logger.info("Starting local PDF sync job")

    storage = S3Storage(
        bucket_name=settings.S3_BUCKET,
        region=settings.AWS_REGION,
    )

    storage.ensure_bucket_exists()
    storage.enable_versioning()

    uploaded = []

    for filename in os.listdir(settings.LOCAL_PDF_DIR):
        if not filename.endswith(".pdf"):
            continue

        local_path = os.path.join(settings.LOCAL_PDF_DIR, filename)
        s3_key = f"pdfs/{filename}"

        storage.upload_pdf(local_path, s3_key)
        uploaded.append(s3_key)

    return PdfSyncResult(uploaded_files=uploaded)
