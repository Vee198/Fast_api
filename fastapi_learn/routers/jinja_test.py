from fastapi import FastAPI, Request,APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/web",
    tags=['web']
)

#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@router.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})
