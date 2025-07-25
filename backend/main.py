from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files from 'frontend' directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

def html_file(name: str) -> str:
    return os.path.join("frontend", name)

@app.get("/")
def read_index():
    return FileResponse(html_file("index.html"))

@app.get("/about")
def read_about():
    return FileResponse(html_file("about.html"))

@app.get("/services/")
def read_services():
    return FileResponse(html_file("services.html"))

@app.get("/contact")
def get_contact():
    return FileResponse(html_file("contact.html"))

@app.post("/contact")
async def post_contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    print("\n📩 New Contact Submission")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)
    return RedirectResponse(url="/thankyou", status_code=303)

