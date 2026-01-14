from app.core.security import create_access_token

# replace with DB later
FAKE_USERS = {
    "admin": "admin123"
}

class AuthService:
    def authenticate(self, username: str, password: str) -> str | None:
        if FAKE_USERS.get(username) != password:
            return None

        return create_access_token({"sub": username})
