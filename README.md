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
## Deployment Architecture (Day 24)

Initial containerization via Docker was explored.
Due to 4GB RAM constraints on edge hardware, the final production-grade
implementation uses a native Ollama runtime on Windows.

This approach:
- Eliminates container/WSL2 overhead
- Improves system stability
- Maintains strict localhost-only inference
- Ensures GDPR Article 32 compliance (Security of Processing)

The Dockerfile is retained for reference and higher-resource environments.
Day 24 confirms GDPR-first local inference:
- Local Ollama runtime
- Local model storage
- Localhost-only binding
- Offline operation verified
## Day 24 — Local AI GDPR Verification

This project uses a native local LLM runtime (Ollama) to ensure:
- Model weights are stored locally on disk
- Inference runs entirely offline
- The service binds only to 127.0.0.1 (localhost)
- No external APIs or cloud services are used

Verification steps:
- ollama list
- ollama run llama3.2:1b
- netstat -ano | findstr 11434

This satisfies GDPR Article 32 (Security of Processing)
and data residency requirements for EU/CH RegTech systems.