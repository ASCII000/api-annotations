import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

import uvicorn

from src.settings import settings

# Instancias fastapi jinja templates, e entregar arquivos estaticos
app = FastAPI()
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    password: str = Form(...),
):

    if password != settings.APP_TOKEN:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Senha inválida"})

    response = RedirectResponse("/annotations", status_code=302)
    response.set_cookie("token", settings.APP_TOKEN)

    return response

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("token")

    return response

from src.routes.annotations import router as annotations_router
app.include_router(annotations_router, prefix="/annotations", tags=["annotations"])

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
