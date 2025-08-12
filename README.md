# 🧱 FastAPI Clean Architecture Template

A scalable, maintainable and production-ready project template for building APIs using **FastAPI**, following the principles of **Clean Architecture**, **Domain-Driven Design (DDD)** and **Service Layer Pattern**.

This template provides a modular structure that separates concerns across different layers of the application, making it easier to test, extend and scale over time.

---

## 🚀 Features

- ✅ Clean project structure with clear separation of concerns
- ✅ Dependency Injection ready
- ✅ SQLAlchemy ORM integration
- ✅ Pydantic schemas for data validation and serialization
- ✅ Service and Repository layers
- ✅ Enum-based roles for cleaner domain logic
- ✅ Middleware for response size logging
- ✅ Seed system for default roles and users
- ✅ Integrated test suite using **pytest**
- ✅ Modular and versioned API routing

---

## 🗂️ Project Structure

```text
├── app
│ ├── api
│ │ └── v1
│ │     └── routes
│ │         ├── auth.py
│ │         ├── role.py
│ │         └── user.py
│ ├── core
│ │ ├── config.py
│ │ ├── logging.py
│ │ └── security.py
│ ├── db
│ │ ├── base.py
│ │ ├── seed
│ │ │ ├── role_seed.py
│ │ │ └── user_seed.py
│ │ └── session.py
│ ├── enums
│ │ └── role.py
│ ├── main.py
│ ├── middleware
│ │ └── response_size_logger.py
│ ├── models
│ │ ├── role.py
│ │ └── user.py
│ ├── repositories
│ │ ├── role_repository.py
│ │ └── user_repository.py
│ ├── schemas
│ │ ├── role.py
│ │ └── user.py
│ └── services
│     ├── role_service.py
│     └── user_service.py
├── database.db
├── logs
│ └── app.log
├── poetry.lock
├── pyproject.toml
├── pytest.ini
└── tests
    ├── conftest.py
    └── integration
        └── user
            ├── test_create_users.py
            ├── test_delete_users.py
            ├── test_get_users.py
            ├── test_list_users.py
            └── test_update_users.py
```

---

## ⚙️ Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Poetry**
- **Pytest**

---

## 🧪 Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/vinicinhus/fastapi-clean-architecture-template.git

cd fastapi-clean-architecture-template
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Run the Application

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at: <http://localhost:8000>

### 🧪 Running Tests

```bash
poetry run pytest
```

## 📐 Architecture Overview

This project follows a layered architecture inspired by Clean Architecture and DDD:

- **API Layer:** Handles HTTP requests and responses.

- **Service Layer:** Contains application logic (use cases).

- **Repository Layer:** Isolates and abstracts data access logic.

- **Domain Layer:** Models the business entities (SQLAlchemy).

- **Schema Layer:** Handles input/output via Pydantic models.

- **Infrastructure Layer:** Includes logging, security, middleware, and DB setup.
