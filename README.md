# Mini Document API

A simple Document API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis**, and **Pytest**.

This project is built as a practical backend project for learning Python production development and AI backend foundations.

---

## Features

- CRUD API for documents
- PostgreSQL database
- SQLAlchemy ORM
- Redis caching
- Cache invalidation after update/delete
- FastAPI dependency injection
- Pydantic request/response validation
- Pytest API testing
- Pytest fixtures with setup/teardown

---

## Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Redis
- python-jose
- Pytest

---

## Project Structure

```text
mini-document-api/
│
├── src/
│   └── app/
│       ├── main.py
│       │
│       ├── data/
│       │   └── ...
│       │
│       ├── pydantic/
│       │   └── ...
|       |
|       ├── redis/
│       │   └── ...
│       │
│       └── test/
│          └── main_test.py
│
├── .gitignore
├── pyproject.toml
└── README.md
```
