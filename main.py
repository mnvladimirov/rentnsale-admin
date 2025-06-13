from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory="templates")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

items = [
    {"id": 1, "name": "Велотуфли Shimano", "size": "42", "city": "Алматы", "condition": "Б/у", "contact": "@user1"},
    {"id": 2, "name": "Шлем Giro", "size": "M", "city": "Астана", "condition": "Новая", "contact": "@user2"}
]

def is_logged_in(request: Request):
    return request.session.get("logged_in") == True

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    if is_logged_in(request):
        return RedirectResponse("/admin")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["logged_in"] = True
        return RedirectResponse("/admin", status_code=302)
    return RedirectResponse("/", status_code=302)

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request):
    if not is_logged_in(request):
        return RedirectResponse("/")
    return templates.TemplateResponse("admin.html", {"request": request, "items": items})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")
