from fastapi import FastAPI
from db.init_db import init_db

app = FastAPI(
    title="Regulated Intake API",
    version="1.0.0",
)

@app.on_event("startup")
def startup():
    init_db()

from db.routes.ingest import router as ingest_router
from db.routes.documents import router as documents_router
from db.routes.audit import router as audit_router

app.include_router(ingest_router, tags=["Ingest"])
app.include_router(documents_router, tags=["Documents"])
app.include_router(audit_router, tags=["Audit"])
