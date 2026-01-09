from app.services.retrieval_service import SearchService
from app.infra.bedrock_llm_client import generate_completion
from app.core.config_loader import load_prompts



prompts = load_prompts()
RAG_PROMPT = prompts["rag"]

class RAGService:
    def __init__(self):
        self.search = SearchService()

    async def answer(self, query: str, top_k: int = 5) -> str:
        # Retrieve
        result = self.search.hybrid_search(query, top_k=top_k)

        hits = result["hits"]["hits"]
        if not hits:
            return "No relevant documents found."

        # Build context
        context_chunks = [
            hit["_source"]["content"]
            for hit in hits
            if "content" in hit["_source"]
        ]

        context = "\n\n---\n\n".join(context_chunks)

        # Prompt
        prompt = RAG_PROMPT["template"] \
            .replace("{{system_prompt}}", RAG_PROMPT["system_prompt"]) \
            .replace("{{context}}", context) \
            .replace("{{query}}", query)

        # Generate
        return await generate_completion(prompt)
