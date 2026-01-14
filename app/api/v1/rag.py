from fastapi import APIRouter, Depends
from app.schemas.rag import RAGRequest, RAGResponse
from app.api.deps import get_current_user
from app.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["RAG"])

def get_rag_service():
    return RAGService()

@router.post("/answer", response_model=RAGResponse)
async def rag_answer(
    payload: RAGRequest,
    user: str = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
):
    answer = await rag_service.answer(
        query=payload.query,
        top_k=payload.top_k,
    )
    return RAGResponse(answer=answer)
