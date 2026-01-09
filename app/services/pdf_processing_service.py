from langchain_community.document_loaders import PyPDFLoader
from app.core.logger import get_logger

logger = get_logger(__name__)


def pdf_to_markdown(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    logger.info("Extracted %d pages from PDF", len(docs))

    md_content = []

    for i, doc in enumerate(docs, start=1):
        md_content.append(f"## Page {i}\n")
        md_content.append(doc.page_content.strip())
        md_content.append("\n")

    return "\n".join(md_content)
