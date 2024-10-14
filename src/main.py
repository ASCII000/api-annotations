import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, Request, Body
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

import uvicorn

from src.settings import settings


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
    token = request.cookies.get("token")

    if token == settings.APP_TOKEN:
        return RedirectResponse("/annotations", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    password: str = Body(..., embed=True),
):
    if password != settings.APP_TOKEN:
        return JSONResponse({"error": "Senha inválida"}, status_code=401)
    
    response = RedirectResponse(url="/annotations", status_code=302)
    response.set_cookie(key="token", value=settings.APP_TOKEN, max_age=86400, httponly=True, secure=True, samesite="strict")
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
