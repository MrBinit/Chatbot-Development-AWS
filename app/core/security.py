from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import get_settings



ALGORITHM = "HS256" # just hard coded for the demo
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
