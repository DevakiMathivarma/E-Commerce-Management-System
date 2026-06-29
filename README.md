# E-Commerce Order Management System (FastAPI)

## Project Overview

The E-Commerce Order Management System is a RESTful backend application developed using FastAPI. It provides authentication, role-based authorization, product management, shopping cart functionality, order processing, payment management, filtering, pagination, logging, Docker support, and unit testing.

---

# Tech Stack

* Python 3.11
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Uvicorn
* Pytest
* Docker

---

# Project Structure

```
project/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── routes/
│   ├── utils/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── seed.py
│
├── tests/
│
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# Setup Instructions

### Clone the Repository

```bash
git clone <your-github-repository-url>
```

```bash
cd E-commerce
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Database Migration

```bash
python app/seed.py
```

or create the database tables automatically by running

```bash
uvicorn app.main:app --reload
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# Environment Variables

Create a `.env` file in the project root.

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./ecommerce.db
```

---

# Authentication Flow

### Register

```
POST /api/v1/auth/register
```

Registers a new customer.

---

### Login

```
POST /api/v1/auth/login
```

Returns a JWT Access Token.

Example Response

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

---

### Authorization

Click **Authorize** in Swagger.

Enter

```
Bearer <your_access_token>
```

All secured endpoints will now be accessible according to the user's role.

---

# API Flow Overview

## Authentication

* POST /api/v1/auth/register
* POST /api/v1/auth/login

---

## Product Management

* POST /api/v1/products
* GET /api/v1/products
* GET /api/v1/products/{id}
* PUT /api/v1/products/{id}
* DELETE /api/v1/products/{id}

---

## Shopping Cart

* POST /api/v1/cart/add
* GET /api/v1/cart
* DELETE /api/v1/cart/remove/{product_id}

---

## Order Management

* POST /api/v1/orders
* GET /api/v1/orders
* GET /api/v1/orders/{id}

---

## Payment Management

* POST /api/v1/payments/{order_id}
* GET /api/v1/payments/{payment_id}

---

# Features Implemented

* JWT Authentication
* Role-Based Authorization
* Product CRUD
* Soft Delete
* Shopping Cart
* Order Management
* Payment Processing
* Pagination
* Filtering
* Logging
* Docker Support
* Swagger Documentation
* Unit Testing using Pytest

---

# Business Rules

* Email must be unique.
* Product name must be unique.
* Product price must be greater than zero.
* Product stock cannot be negative.
* Customers cannot add inactive products to the cart.
* Customers cannot order quantities greater than available stock.
* Order total is calculated automatically.
* Product stock is reduced after order confirmation.
* Duplicate payments are prevented.
* Payment amount must exactly match the order amount.
* Customers can only access their own cart, orders, and payments.
* Only administrators can manage products.

---

# Assumptions Made

* SQLite is used as the database.
* JWT is used for authentication.
* One customer owns one shopping cart.
* One cart can contain multiple cart items.
* One order contains multiple order items.
* One order can have only one successful payment.
* Soft delete is implemented using the `is_active` field.
* Product stock is updated when an order is successfully created.
* Admin users manage products, while customers manage their own carts, orders, and payments.

---

# Running Unit Tests

```bash
pytest
```

or

```bash
pytest -v
```

---

# Docker

Build Docker Image

```bash
docker build -t ecommerce-app .
```

Run Docker Container

```bash
docker run -d -p 8000:8000 ecommerce-app
```

---

# Logging

Application logs are stored in

```
logs/app.log
```

Logs are also displayed in the terminal during application execution.

---

# GitHub Repository

```
https://github.com/DevakiMathivarma/E-Commerce-Management-System.git
```


