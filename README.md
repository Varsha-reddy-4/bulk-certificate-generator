# Bulk Certificate Generator

A REST API for generating participation certificates in bulk for multiple recipients.

This project was developed as a backend practical assignment using Python, FastAPI, MySQL, SQLAlchemy, Pydantic, and ReportLab.

---

## Project Overview

The Bulk Certificate Generator allows users to submit a list of recipients and generate individual PDF certificates for each recipient.

For every bulk generation request, the application creates a job and tracks:

- Total number of certificates
- Successfully generated certificates
- Failed certificates
- Overall job status
- Individual certificate status
- Generated certificate file path
- Error information for failed certificates

The application uses a relational MySQL database to store job and certificate information.

---

## Features

- Bulk certificate generation
- RESTful API using FastAPI
- MySQL relational database
- SQLAlchemy ORM
- Input validation using Pydantic
- PDF certificate generation using ReportLab
- Job status tracking
- Success and failure tracking
- Individual certificate status tracking
- Individual certificate PDF retrieval
- API documentation using Swagger/OpenAPI
- Automated API testing using pytest
- Environment-based database configuration
- Error handling for individual certificate generation

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| MySQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request validation |
| ReportLab | PDF certificate generation |
| Pytest | Automated testing |
| HTTPX | API testing |
| Uvicorn | Application server |

---

## System Architecture

```text
Client
   |
   v
FastAPI REST API
   |
   +--------------------+
   |                    |
   v                    v
Pydantic Validation   Job Processing
                         |
                         +-------------------+
                         |                   |
                         v                   v
                    MySQL Database       ReportLab
                         |                   |
                         v                   v
                   Job & Certificate    PDF Files
                       Records          (generated/)


bulk-certificate-generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── jobs.py
│   │
│   └── services/
│       ├── __init__.py
│       └── certificate.py
│
├── generated/
│
├── tests/
│   └── test_jobs.py
│
├── .gitignore
├── .env
├── requirements.txt
└── README.md

Run Project: venv\Scripts\activate
uvicorn app.main:app --reload
pytest