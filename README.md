
# User Management Backend

Backend-only project built using **Core Django (without Django REST Framework)**.
Implements custom authentication, session handling, role management, and soft delete functionality using PostgreSQL.

---

## Tech Stack

* Python
* Django
* PostgreSQL
* psycopg2-binary

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2. Install Dependencies

```bash
pip install django psycopg2-binary
```

### 3. Configure Database

Update `settings.py` with your PostgreSQL credentials.

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Server

```bash
python manage.py runserver
```

---

## Features

* Custom user registration
* Password hashing
* Session-based login & logout
* Role-based access control
* Soft delete using `is_active`
* Protected endpoints via custom decorator

---
