# Greatcart — E‑commerce (Django)

A full-stack style e-commerce web application built with **Django 6**. It provides product browsing, user accounts, a session-based shopping cart with coupons, and checkout with order management.

## Features

- **Catalog** — Home page, category pages, product detail pages, product listing, and search
- **Products** — Categories, featured items, pricing, stock flag, image thumbnails, homepage sliders (admin-uploaded banners)
- **Accounts** — Custom user model, registration, login/logout, change password, email-based password reset
- **Cart** — Add items, view cart, apply discount coupons (with minimum-order rules where configured)
- **Orders** — Checkout flow with shipping details; orders tied to users with status tracking

## Tech stack

- Python 3
- Django 6.x
- SQLite (default; suitable for development)
- Server-rendered templates with static assets

Optional but recommended for image uploads (e.g. slider banners): **Pillow**.

## Project layout

```
e-com_Project/
└── greatcart/                 # Django project root (run commands from here)
    ├── manage.py
    ├── greatcart/             # Settings & root URL config
    ├── product/
    ├── user_account/
    ├── cart/
    ├── order/
    ├── templates/
    ├── static/
    └── media/                 # User/media uploads (created at runtime)
```

## Prerequisites

- Python 3.10+ (use a version compatible with your installed Django release)
- `pip` and a virtual environment (recommended)

## Setup

1. **Clone the repository** (or extract the project) and go to the Django project directory:

   ```bash
   cd greatcart
   ```

2. **Create and activate a virtual environment** (example):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install "Django>=6.0,<7" Pillow
   ```

4. **Apply migrations** and create an admin user if you need the Django admin:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The admin site is at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Configuration notes

- **Database** — Default is SQLite (`db.sqlite3` under `greatcart/`). For production, point `DATABASES` in `greatcart/greatcart/settings.py` to PostgreSQL or another supported backend.
- **Email** — Password reset uses Django’s email stack. SMTP settings live in `settings.py`. For any shared or public repo, move secrets (`SECRET_KEY`, email password, etc.) into environment variables and reference them from settings instead of committing real credentials.
- **Debug & hosts** — `DEBUG` and `ALLOWED_HOSTS` are set for local development. Harden both before deploying.

## Main URL routes (high level)

| Area        | Examples |
|------------|-----------|
| Storefront | `/`, `/product-details/<slug>/`, `/category-details/<slug>/`, `/product-list/`, `/search-products/` |
| Account    | `/login/`, `/logout/`, `/registration/`, `/change-password/`, `/password-reset/` |
| Cart       | `/add-to-cart/<id>/`, `/cart/`, `/add-coupon/` |
| Checkout   | `/checkout/` |
| Admin      | `/admin/` |


