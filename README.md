# 🚀 Dar-techXSolutions — FastAPI Web App

This project is a full-featured FastAPI-based web application with session-based authentication, templated UI using Jinja2, and deploy-ready setup for Render.

## ✨ Features

* FastAPI + Jinja2 templates
* Static file support (CSS, images)
* User Signup/Login (session-based)
* Protected routes: dashboard, profile, settings
* Contact form with POST/Redirect
* Responsive HTML layout with `base.html`

## 📁 Project Structure

```
project-root/
├── backend/
│   └── main.py
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html, about.html, etc.
│   └── static/
│       └── styles/style.css
├── requirements.txt
├── render.yaml
├── README.md
```

## 🛠 Requirements

```bash
pip install -r requirements.txt
```

## 🚀 Run Locally

```bash
uvicorn backend.main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

## 🧪 Test Auth Flow

1. Visit `/signup` → create account
2. Auto-login to `/dashboard`
3. Logout → test access block on `/profile`, etc.

## 🌐 Deploy on Render

1. Push project to GitHub
2. Create `render.yaml` with:

```yaml
services:
  - type: web
    name: dartechx-app
    env: python
    plan: free
    buildCommand: ""
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

3. Login to [render.com](https://render.com), click **New Web Service**, and connect your repo.

## 🧩 License

© 2025 Dar-techXSolutions — All rights reserved.
