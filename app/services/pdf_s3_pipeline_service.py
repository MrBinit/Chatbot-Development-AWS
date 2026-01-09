import os
from app.core.config import settings
from app.core.logger import get_logger
from app.infra.s3_bucket import S3Storage
from app.services.pdf_processing_service import pdf_to_markdown

logger = get_logger(__name__)


def process_pdfs_from_s3():
    storage = S3Storage(
        bucket_name=settings.S3_BUCKET,
        region=settings.AWS_REGION,
    )

    os.makedirs("data/tmp_pdfs", exist_ok=True)
    os.makedirs("data/extracted_data", exist_ok=True)

    bucket = storage.bucket

    for obj in bucket.objects.filter(Prefix="pdfs/"):
        if not obj.key.endswith(".pdf"):
            continue

        filename = os.path.basename(obj.key)
        local_pdf = f"data/tmp_pdfs/{filename}"
        md_output = f"data/extracted_data/{filename.replace('.pdf', '.md')}"

        logger.info("Processing S3 PDF: %s", obj.key)
        try:
            # Download
            storage.download_pdf(obj.key, local_pdf)
            # extracts the pdf to markdown format.
            md_text = pdf_to_markdown(local_pdf)
            with open(md_output, "w", encoding="utf-8") as f:
                f.write(md_text)

            logger.info("Saved extracted markdown to %s", md_output)
        finally:
            if os.path.exists(local_pdf):
                os.remove(local_pdf)
                logger.info("Deleted temp file %s", local_pdf)
