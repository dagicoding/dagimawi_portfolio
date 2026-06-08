# Dagimawi Tarekegne — Portfolio Website

A complete Django portfolio website with a **custom admin dashboard** and **email notifications**.

## Quick Start

```bash
unzip dagimawi_portfolio.zip
cd dagimawi_portfolio
bash setup.sh
```

Then run:
```bash
source venv/bin/activate
python manage.py runserver
```

## URLs

| Page | URL |
|---|---|
| Website | http://127.0.0.1:8000/ |
| **Custom Dashboard** | **http://127.0.0.1:8000/dashboard/** |
| Django Admin (backup) | http://127.0.0.1:8000/admin/ |

> Login to the dashboard with your superuser credentials (created during setup).

---

## Custom Dashboard Sections

| Section | What you manage |
|---|---|
| **Overview** | Stats cards, recent messages & works, quick actions |
| **Profile & Roles** | Name, bio, photo, CV, typing animation roles |
| **Works** | Add/edit/delete projects, toggle featured & visible |
| **Skills** | Skill bars with percentages and icons |
| **Statistics** | Counter numbers (50+ Projects, etc.) |
| **Services** | Services shown on About page |
| **Experience** | Work history timeline |
| **Testimonials** | Client reviews with star ratings |
| **Social Links** | All social media URLs |
| **Contact Info & Email** | Email/phone/address + email notification target |
| **Announcements** | Glassmorphism popup announcements |
| **Messages Inbox** | Read, reply, archive, delete contact messages |

---

## Email Notifications Setup

When someone submits your contact form, an email is sent to the address in **Dashboard → Contact Info**.

### Step 1 — Enable Gmail SMTP

Open `dagimawi_portfolio/settings.py` and replace the email section:

```python
EMAIL_BACKEND    = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST       = 'smtp.gmail.com'
EMAIL_PORT       = 587
EMAIL_USE_TLS    = True
EMAIL_HOST_USER  = 'your_gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'   # Not your real password!
DEFAULT_FROM_EMAIL = 'Dagimawi Portfolio <your_gmail@gmail.com>'
```

### Step 2 — Get a Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → 2-Step Verification (must be enabled)
3. Security → App Passwords
4. Create one for "Mail" → copy the 16-character password
5. Paste it as `EMAIL_HOST_PASSWORD`

### Step 3 — Set recipient email

Go to **Dashboard → Contact Info** and set your email address. All form submissions will be forwarded there.

> In development, emails print to the terminal console instead of sending. All messages are always saved to the database regardless.

---

## Project Structure

```
dagimawi_portfolio/
├── dagimawi_portfolio/
│   ├── settings.py          ← Email config here
│   └── urls.py
├── portfolio/
│   ├── models.py            ← All 12 database models
│   ├── views.py             ← Public pages + full dashboard views
│   ├── urls.py              ← All routes incl. /dashboard/*
│   ├── admin.py             ← Django admin config
│   ├── forms.py             ← Contact form
│   ├── context_processors.py
│   ├── templates/
│   │   ├── portfolio/       ← 9 public page templates
│   │   └── dashboard/       ← 16 dashboard templates
│   └── static/portfolio/
│       ├── css/main.css     ← Dark/light mode, glassmorphism
│       └── js/main.js       ← Typed, lightbox, AJAX, etc.
├── media/                   ← Uploaded files
├── requirements.txt
├── setup.sh                 ← One-command setup
└── manage.py
```

## Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Use a strong random `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Switch to PostgreSQL
- [ ] Configure Gmail SMTP (or SendGrid/Mailgun)
- [ ] Set up WhiteNoise or Nginx for static files
- [ ] Use `gunicorn` or `uvicorn` as WSGI server
