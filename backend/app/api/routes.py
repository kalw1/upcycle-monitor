"""HTTP API routes."""

from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter()

@router.post("/metrics", tags=["metrics"])
def metrics(payload: dict[str, Any], db: Session = Depends(get_db)) -> dict[str, str]:
    """Gathering of data from exporter."""



    return {"status": "ok"}

@router.get("/health", tags=["health"])
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    """Report service and database readiness."""

    db.execute(text("SELECT 1"))
    return {"status": "ok"}
