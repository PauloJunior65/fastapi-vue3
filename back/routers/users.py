from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from utils.babel import _,templates

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    return {"message": _("Teste 1")}

@router.get("/items", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("items.html", {"request": request})