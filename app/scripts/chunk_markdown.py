from pathlib import Path
from app.services.markdown_chunking_service import chunk_legal_markdown
from app.services.embedding_service import embed_chunks

md_path = Path("data/extracted_data/National AI Policy.md")
text = md_path.read_text(encoding="utf-8")

chunks = chunk_legal_markdown(text, md_path.name)

embedded = embed_chunks(chunks)

print(f"Embedded {len(embedded)} chunks")
