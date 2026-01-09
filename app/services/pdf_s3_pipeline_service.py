import os

from app.core.logger import get_logger
from app.core.config_loader import load_app_config
from app.infra.s3_bucket import S3Storage
from app.services.pdf_processing_service import pdf_to_markdown

logger = get_logger(__name__)

# Load once (cached)
app_config = load_app_config()

AWS_REGION = app_config["aws"]["region"]
S3_BUCKET = app_config["storage"]["s3_bucket"]

TMP_PDF_DIR = "data/tmp_pdfs"
EXTRACTED_DATA_DIR = "data/extracted_data"


def process_pdfs_from_s3():
    storage = S3Storage(
        bucket_name=S3_BUCKET,
        region=AWS_REGION,
    )

    os.makedirs(TMP_PDF_DIR, exist_ok=True)
    os.makedirs(EXTRACTED_DATA_DIR, exist_ok=True)

    bucket = storage.bucket

    for obj in bucket.objects.filter(Prefix="pdfs/"):
        if not obj.key.endswith(".pdf"):
            continue

        filename = os.path.basename(obj.key)
        local_pdf = os.path.join(TMP_PDF_DIR, filename)
        md_output = os.path.join(
            EXTRACTED_DATA_DIR,
            filename.replace(".pdf", ".md"),
        )

        logger.info("Processing S3 PDF: %s", obj.key)

        try:
            storage.download_pdf(obj.key, local_pdf)

            md_text = pdf_to_markdown(local_pdf)
            with open(md_output, "w", encoding="utf-8") as f:
                f.write(md_text)

            logger.info("Saved extracted markdown to %s", md_output)

        finally:
            if os.path.exists(local_pdf):
                os.remove(local_pdf)
                logger.info("Deleted temp file %s", local_pdf)
