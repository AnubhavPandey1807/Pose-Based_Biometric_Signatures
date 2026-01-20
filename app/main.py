from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import auth

app = FastAPI()

# ✅ Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ Templates
templates = Jinja2Templates(directory="app/templates")

# ✅ Routers
app.include_router(auth.router, prefix="/auth")



@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
