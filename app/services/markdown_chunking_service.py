import os
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
BASE_CHUNK_DIR = "data/chunks"


def chunk_legal_markdown(md_text: str, source_name: str) -> List[Document]:
    """
    Chunk a legal / policy Markdown document using:
    1) Markdown header-based chunking
    2) Recursive fallback for oversized sections
    """

    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]

    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    header_chunks = md_splitter.split_text(md_text)

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )

    final_chunks: List[Document] = []

    for chunk in header_chunks:
        base_metadata = {
            "source": source_name,
            **chunk.metadata,
        }

        if len(chunk.page_content) <= MAX_CHUNK_SIZE:
            final_chunks.append(
                Document(
                    page_content=chunk.page_content,
                    metadata=base_metadata,
                )
            )
        else:
            sub_chunks = recursive_splitter.split_text(chunk.page_content)

            for idx, sub_text in enumerate(sub_chunks):
                final_chunks.append(
                    Document(
                        page_content=sub_text,
                        metadata={
                            **base_metadata,
                            "sub_chunk": idx,
                        },
                    )
                )

    return final_chunks


def save_chunks(chunks: List[Document], source_name: str) -> None:
    """
    Persist chunks to disk under data/chunks/<document_name>/
    """

    doc_dir = os.path.join(
        BASE_CHUNK_DIR,
        source_name.replace(".md", "")
    )
    os.makedirs(doc_dir, exist_ok=True)

    for idx, chunk in enumerate(chunks, start=1):
        chunk_path = os.path.join(doc_dir, f"chunk_{idx:03d}.md")

        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk.page_content)
