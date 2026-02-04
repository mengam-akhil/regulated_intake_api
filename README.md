<<<<<<< HEAD
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
"Used for load balancers and container health probes"

=======
>>>>>>> 6c290fb (Day 14:Persistence & audit trail with SQLite completed)
## Persistence & Audit Trail (Day 14)
-SQLite-backed document traceability
-Audit logs for regulatory reconstruction
This enables full regulatory tracebility and post-event reconstruction of ingestion decisions 
# Regulated Intake API

![CI](https://github.com/mengam-akhil/regulated-intake-api/actions/workflows/ci.yml/badge.svg)
![Security](https://img.shields.io/badge/security-pip--audit-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)

A secure, audit-ready API for regulated data ingestion with validation, logging, and CI/CD.
