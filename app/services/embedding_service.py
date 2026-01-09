from typing import List
from langchain_core.documents import Document
from app.infra.bedrock_embedding_client import EmbeddingBedrockClient
from app.core.logger import get_logger

logger = get_logger(__name__)

client = EmbeddingBedrockClient()

def embed_chunks(chunks: List[Document]) -> List[dict]:
    results = []

    for idx, chunk in enumerate(chunks):
        logger.info("Embedding chunk %d", idx + 1)

        embedding = client.embed_text(chunk.page_content)

        logger.info("Embedding dimension: %d", len(embedding))

        results.append({
            "embedding": embedding,
            "text": chunk.page_content,
            "metadata": chunk.metadata,
        })

    return results
