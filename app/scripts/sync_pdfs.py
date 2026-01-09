from app.core.logger import get_logger
from app.services.pdf_sync_service import sync_local_pdfs

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("PDF sync script started")

    result = sync_local_pdfs()

    logger.info("PDF sync script finished successfully")
    logger.info("Uploaded files: %s", result.uploaded_files)
