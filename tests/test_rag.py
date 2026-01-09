import asyncio
from app.services.rag_service import RAGService

async def main():
    rag = RAGService()
    query = "What is the National AI Policy about?"
    answer = await rag.answer(query, top_k=5)

    print("\n=== RAG ANSWER ===")
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
