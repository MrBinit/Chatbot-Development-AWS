from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    token = auth_service.authenticate(
        payload.username,
        payload.password
    )

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenResponse(access_token=token)
