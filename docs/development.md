# Development

## Backend

Create and install the backend environment from `backend/`:

```shell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[test]"
uvicorn app.main:app --reload
```

The backend defaults to SQLite at `backend/data/upcycle-monitor.db`. Override
the database and CORS settings with the `UPCYCLE_MONITOR_` environment
variables documented in [`backend/README.md`](../backend/README.md).

Backend tests can be run from `backend/` with:

```shell
python -m pytest
```
