from app.core.logger import get_logger
from app.services.pdf_s3_pipeline_service import process_pdfs_from_s3

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting S3 → PDF → Markdown pipeline")
    process_pdfs_from_s3()
    logger.info("Pipeline completed successfully")
