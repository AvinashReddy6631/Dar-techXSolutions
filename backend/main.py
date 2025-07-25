# backend/main.py (toast version, email .env safe loading)
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# In-memory "user db"
users = {}

def get_current_user(request: Request):
    return request.session.get("user")

# Send contact notification email (to yourself)
def notify_admin(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = "📨 New Contact Form Submission"

    from_email = os.getenv("EMAIL_FROM")
    to_email = os.getenv("EMAIL_TO")
    from_pass = os.getenv("EMAIL_PASS")

    if not from_email or not from_pass or not to_email:
        print("❌ Missing EMAIL_FROM, EMAIL_PASS, or EMAIL_TO in .env")
        return

    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(f"""
    Name: {name}
    Email: {email}
    Message:
    {message}
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, from_pass)
            smtp.send_message(msg)
            print("✅ Notification email sent successfully")
    except Exception as e:
        print("⚠️ Email notification failed:", e)

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
    notify_admin(name, email, message)
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
