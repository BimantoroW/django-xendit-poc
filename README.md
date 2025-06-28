# Django Xendit Demo

Django application to demonstrate a complete e-commerce checkout flow with the Xendit payment gateway. The app allows users to register, add courses to a cart, and complete purchases via Xendit. Upon successful payment, users are granted access to their purchased courses.

**Tech Stack:** Django | PostgreSQL | Docker | Xendit API

## Deployed Application

**Live URL:** [http://34.81.22.12](http://34.81.22.12)

## Core Features & Assignment Requirements

This project has implemented all requirements outlined in the assignment description.

* **Payment Gateway Integration**: Securely integrated with Xendit to handle payments via Virtual Account, Debit/Credit Card, and QRIS.

* **Dummy Content & Protected Access**: The application is seeded with three dummy courses that users can purchase. A course details page is the "paid feature", which is only accessible after a user has successfully purchased the course.

* **Authentication**: User registration and login was implemented to support a shopping cart system and user-specific enrollments. While noted as optional, this was included to build a more robust and realistic application.

* **Deployment**: The application is fully containerized with Docker and includes configurations for Nginx.

## The Order and Payment Flow

The checkout process is designed to robustly handle interaction between the user, the server, and the external Xendit gateway.

1.  **Order Creation**:
    - When a user initiates checkout, an `Order` object with a `PENDING` status is created in the database. This is created in a `transaction.atomic()` block to protect data consistency in the event of a database error.
    - An API call is then made to Xendit with the order details. Xendit sends back a URL containing the invoice, and the user is redirected there to complete their payment.
    - The user's `Cart` is only deleted after a successful API response from Xendit is received. If the API call fails, the user is redirected back to their cart with its contents intact.

2.  **Webhook Handling**:
    - After the user is redirected and successfully pays, Xendit will send a webhook to the server to notify of the payment.
    - A dedicated endpoint listens for that webhook from Xendit.
    - The endpoint first validates the `X-Callback-Token` header from the incoming request against the real Xendit callback token.
    - If the token is valid and the payment status is `PAID`, the corresponding `Order` status is updated, and `Enrollment` records are created to grant the user access to the courses.

3.  **Frontend and Backend Synchronization**:
    - After payment, the user will be redirected a `Payment Processing` page.
    - This page uses JavaScript to poll an API endpoint on the server every few seconds. This API endpoint will respond with the status of the user's invoice.
    - The user is only redirected to the final success page after the polling API confirms the order status is `PAID`. This prevents a condition where the user might see a success page before the server has received the payment webhook from Xendit.

## Installation 

### Python

```bash
# Clone the repository
git clone https://github.com/BimantoroW/django-xendit-poc.git
cd django-xendit-poc

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run database migrations
python manage.py migrate

# Seed database with dummy courses
python3 manage.py seed

# Start server
python3 manage.py runserver
```

### Docker

```bash
# Clone the repository
git clone https://github.com/BimantoroW/django-xendit-poc.git
cd django-xendit-poc

# Create .env.prod file
cp .env.example .env.prod

# Please adjust the exposed port of nginx in docker-compose.yml before starting
docker compose up -d --build
```