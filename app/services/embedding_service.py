from typing import List
from langchain_core.documents import Document
from app.infra.bedrock_embedding_client import EmbeddingBedrockClient
from app.core.logger import get_logger

logger = get_logger(__name__)

client = EmbeddingBedrockClient()

def embed_chunks(chunks: List[Document]) -> List[dict]:
    results = []

    for idx, chunk in enumerate(chunks):
        text = chunk.page_content.strip()

        if not text:
            logger.warning("Skipping empty chunk at index %d", idx)
            continue

        embedding = client.embed_text(text)

        if embedding is None:
            logger.error("Embedding returned None at index %d", idx)
            continue

        if not isinstance(embedding, list):
            logger.error("Embedding is not a list at index %d", idx)
            continue

        if len(embedding) != 1024:
            logger.error(
                "Embedding dimension mismatch at index %d: got %d",
                idx,
                len(embedding),
            )
            continue

        results.append({
            "embedding": embedding,
            "text": text,
            "metadata": chunk.metadata,
        })

    return results
