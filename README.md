# NezShop

E-commerce backend built with Django and Django REST Framework.

## Features

- **Accounts** — OTP authentication, user profile and addresses
- **Products** — Product and brand management, filtering and search
- **Cart** — Shopping cart
- **Order** — Orders and checkout
- **Discount** — Discount codes
- **Payment** — Payment
- **Report** — Reporting
- API documentation with drf-spectacular (Swagger UI)
- JWT authentication (`djangorestframework_simplejwt`)

## Installation & Setup

1. Clone the project and create a virtual environment:

```bash
   git clone <repo-url>
   cd NezShop_Project
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install the packages:

```bash
   pip install -r requirements.txt
```

3. Set up environment variables:

```bash
   cp .env.example .env
   # then replace the values in .env with your real values
```

4. Run migrations and start the server:

```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
```

5. API documentation:
   - Swagger UI: `/api/schema/swagger-ui/` (depending on the project's urls.py configuration)

## Demo Frontend

The `frontend/index.html` folder is a standalone demo (plain HTML/CSS/JS, no framework) of the storefront — with sample data, a shopping cart, category filtering, and a rotating 3D t-shirt in the hero section. It is not yet connected to the real Django API; just open the file directly in your browser.

## Project Structure
