from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.repo.annotations import AnnotationsRepository
from src.deps.main import verify_token


router = APIRouter()
template = Jinja2Templates(directory="src/templates")
repo = AnnotationsRepository()

@router.get("/")
async def get_annotations(
    request: Request,
    _ = Depends(verify_token)
):
    
    result = repo.get_annotations()  # Obter as anotações
    return template.TemplateResponse("index.html", {"request": request, "annotations": result})
