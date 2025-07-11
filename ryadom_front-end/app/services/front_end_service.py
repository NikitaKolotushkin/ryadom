from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/event/", response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse("event.html", {"request": request})


@router.get("/login/", response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register/", response_class=HTMLResponse)
async def users(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})