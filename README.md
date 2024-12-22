# Django REST API Application

This is a Django-based REST API application that includes **users** and **products** with versioned endpoints. The application supports basic operations (GET, POST, PUT, PATCH, DELETE) for both users and products. Additionally, password management, HTTPS, caching, and versioning are integrated.

## Features
- **Users (v1)**: Create, list, update, and delete users with hashed passwords.
- **Products (v2)**: Create, list, update, and delete products.
- **Caching**: Cached responses for users and products to improve performance.
- **Versioning**: Users are available in API version `v1`, and products are available in API version `v2`.
- **HTTPS**: Secure API using SSL/TLS encryption.
- **Password Management**: Store hashed passwords using Django’s secure hashing.

## Prerequisites
- Python 3.x
- Django 4.x
- Django REST Framework 3.x
- Nginx or other reverse proxy (for production)
- SSL Certificate for HTTPS (e.g., Let's Encrypt)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/django-rest-api.git
    cd django-rest-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser (optional for accessing Django Admin):
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

7. For local HTTPS (optional):
    - Install `django-sslserver`:
      ```bash
      pip install django-sslserver
      ```
    - Add `'sslserver'` to your `INSTALLED_APPS` in `settings.py`.
    - Run the server with SSL:
      ```bash
      python manage.py runsslserver
      ```

## API Endpoints

### **Users (v1)**

- **GET /api/v1/users/**: List all users.
- **POST /api/v1/users/**: Create a new user. (Password is hashed before storing)
    - Example request body:
      ```json
      {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword123"
      }
      ```

- **GET /api/v1/users/{id}/**: Get user details by ID.
- **PUT /api/v1/users/{id}/**: Update user details by ID.
- **PATCH /api/v1/users/{id}/**: Partially update user details by ID.
- **DELETE /api/v1/users/{id}/**: Delete user by ID.

### **Products (v2)**

- **GET /api/v2/products/**: List all products.
- **POST /api/v2/products/**: Create a new product.
    - Example request body:
      ```json
      {
        "name": "Product 1",
        "price": 100.0,
        "description": "This is a sample product."
      }
      ```

- **GET /api/v2/products/{id}/**: Get product details by ID.
- **PUT /api/v2/products/{id}/**: Update product details by ID.
- **PATCH /api/v2/products/{id}/**: Partially update product details by ID.
- **DELETE /api/v2/products/{id}/**: Delete product by ID.

## Caching

The application caches user and product data for better performance. Caching is implemented using Django's caching framework.

- User data is cached for 15 minutes under the key `'v1_users'`.
- Product data is cached for 15 minutes under the key `'v2_products'`.

## Password Management

Passwords are stored securely using Django’s built-in hashing mechanism. When creating or updating a user, the password is hashed before being saved in the database.

- Use `set_password()` method to hash passwords before saving.
- Use `check_password()` to verify a password against the stored hash.

## HTTPS Configuration

### Development
For local development, you can run the server with SSL using `django-sslserver`. This allows testing the application over HTTPS on your local machine.

---