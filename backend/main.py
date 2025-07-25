# backend/main.py (toast version, no thankyou.html)
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# In-memory "user db"
users = {}

def get_current_user(request: Request):
    return request.session.get("user")

# Routes
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": get_current_user(request)})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "user": get_current_user(request)})

@app.get("/services")
def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request, "user": get_current_user(request)})

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "user": get_current_user(request)})

@app.post("/contact")
async def handle_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    print("\n📩 New Contact Submission")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)
    return Response(status_code=204)

@app.get("/dashboard")
def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/profile")
def profile(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.get("/settings")
def settings(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("settings.html", {"request": request, "user": user})

@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users.get(email)
    if user and user["password"] == password:
        request.session["user"] = {"name": user["name"], "email": email}
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    users[email] = {"name": name, "password": password}
    request.session["user"] = {"name": name, "email": email}
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")
