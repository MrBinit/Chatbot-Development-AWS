from pathlib import Path
from app.services.markdown_chunking_service import chunk_legal_markdown
from app.services.embedding_service import embed_chunks
from app.services.vector_store_service import VectorStoreService

md_path = Path("data/extracted_data/National AI Policy.md")
text = md_path.read_text(encoding="utf-8")

# 1. Chunk
chunks = chunk_legal_markdown(text, md_path.name)

# 2. Embed
embedded = embed_chunks(chunks)

# 3. Store in OpenSearch
vector_store = VectorStoreService()
vector_store.store_embeddings(embedded)

print(f"Embedded and stored {len(embedded)} chunks")
