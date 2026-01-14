from app.services.retrieval_service import SearchService
from app.infra.bedrock_llm_client import generate_completion
from app.core.config_loader import load_prompts

prompts = load_prompts()
RAG_PROMPT = prompts["rag"]


class RAGService:
    def __init__(self):
        self._search = None  # lazy

    @property
    def search(self) -> SearchService:
        if self._search is None:
            self._search = SearchService()
        return self._search

    async def answer(self, query: str, top_k: int = 5) -> str:
        result = self.search.hybrid_search(query, top_k=top_k)

        hits = result["hits"]["hits"]
        if not hits:
            return "No relevant documents found."

        context_chunks = [
            hit["_source"]["content"]
            for hit in hits
            if "content" in hit["_source"]
        ]

        context = "\n\n---\n\n".join(context_chunks)

        prompt = (
            RAG_PROMPT["template"]
            .replace("{{system_prompt}}", RAG_PROMPT["system_prompt"])
            .replace("{{context}}", context)
            .replace("{{query}}", query)
        )

        return await generate_completion(prompt)
