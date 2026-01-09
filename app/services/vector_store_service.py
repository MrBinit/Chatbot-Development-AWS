from typing import List
from app.repositories.vector_repository import VectorRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

class VectorStoreService:
    def __init__(self):
        self.repo = VectorRepository()

    def store_embeddings(self, embedded_chunks: List[dict]):
        for idx, chunk in enumerate(embedded_chunks):
            logger.info("Storing chunk %d", idx + 1)

            self.repo.insert_chunk(
                text=chunk["text"],
                embedding=chunk["embedding"],
                metadata=chunk["metadata"],
            )
