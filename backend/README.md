# Backend

The backend is a FastAPI service with a SQLAlchemy 2.x persistence boundary.
SQLite is used by default for local development; production deployments should
provide a mounted data directory or another database URL.

## Setup

From this directory:

```shell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[test]"
```

Optional settings use the `UPCYCLE_MONITOR_` environment prefix:

- `UPCYCLE_MONITOR_DATABASE_URL` — SQLAlchemy database URL.
- `UPCYCLE_MONITOR_CORS_ORIGINS` — JSON list of allowed browser origins.
- `UPCYCLE_MONITOR_ENVIRONMENT` — deployment environment name.

## Run

```shell
uvicorn app.main:app --reload
```

The readiness endpoint is available at `GET /health`.

Telemetry ingestion, historical metrics, power events, and alerts will be
added once their API contracts are defined.
