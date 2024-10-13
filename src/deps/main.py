from fastapi import Request
from fastapi.exceptions import HTTPException

from src.settings import settings


def verify_token(request: Request) -> bool:

    token = request.cookies.get("token")

    if token != settings.APP_TOKEN:
        raise HTTPException(status_code=401, detail="Nao autorizado")
    return True
