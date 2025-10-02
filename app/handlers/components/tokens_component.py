import secrets
import string

ALPHABET = string.ascii_letters + string.digits

async def generate_access_token(length: int = 64) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))