# Billing App – Simple Run Guide

This is a Django billing application packed with Docker, so you **don’t need to install Python or PostgreSQL** on your computer.

---

## What you need first

Make sure you have installed:

* Docker Desktop

That’s all.

---

## Step 1 – Download the project

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## Step 2 – Create environment file

Create a file named:

```
.env.prod
```

Paste this inside:

```env
DEBUG=False
SECRET_KEY=change-this-key
ALLOWED_HOSTS=*

DB_NAME=billing
DB_USER=billing_user
DB_PASSWORD=billing_pass
DB_HOST=db
DB_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

You can change the username and password later.

---

## Step 3 – Run the app

```bash
docker compose up --build
```

Wait until Django finishes starting.

---

## Step 4 – Open in browser

### Shop page

```
http://localhost:8000/shop
```

### Bill page example

```
http://localhost:8000/shop/bill/1/
```

### Customer purchases page

```
http://localhost:8000/shop/customer-purchases/
```

### Admin panel

```
http://localhost:8000/admin
```

Login with:

* **Username:** admin
* **Password:** admin123

---

## Useful commands

### Stop the app

```bash
docker compose down
```

### Reset database completely

```bash
docker compose down -v
```

### Create another admin user manually

```bash
docker compose exec web python manage.py createsuperuser
```

---

## That’s it

If something doesn’t work, restart Docker and run the project again.

The whole system (database and Django app) runs automatically inside Docker.
