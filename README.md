# Regulated Intake API

A compliance-oriented backend API that ingests unstructured regulated data
(FinTech-first, HealthTech-extensible) and converts it into validated,
structured, audit-ready JSON.

This project simulates how regulated systems accept and process sensitive data
using schema validation, domain routing, and traceable request handling.

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## Current Features (Day 9)

- Async `/ingest` endpoint
- Regulated intake envelope (`domain` + `payload`)
- Domain-based routing:
  - FinTech (primary)
  - Health (secondary)
- Strict schema validation
- UUID-based request tracking
- Clean 200 / 422 responses
- Swagger UI for testing

---

## API Endpoints

### Health Check

