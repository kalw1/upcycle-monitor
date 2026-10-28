# upcycle-monitor
Lightweight home-lab monitor dashboard to track system statistics - specifically oriented towards recycled laptop home-labs and their battery/power status.

## Repository layout

The repository is arranged around three independently deployable areas:

- `exporter/` — lightweight telemetry collection on the physical host.
- `backend/` — FastAPI service and SQLite persistence boundary.
- `frontend/` — React/TypeScript dashboard boundary.
- `deploy/` — future container deployment definitions.
- `docs/` — architecture, development, and telemetry notes.

## Important constraints

Battery and AC telemetry should be verified on the physical laptop because it may not be exposed inside a VM or LXC. A powered-off host cannot report its own outage, so future uptime detection will need an external observer or heartbeat consumer.
