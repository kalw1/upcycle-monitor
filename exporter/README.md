# Host Exporter

The exporter runs directly on the physical Proxmox host so it can access
host-specific battery and AC telemetry. It is installed as a Python package
inside a dedicated virtual environment.

## Install on the host

From the deployed exporter directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install .
```

Install the service unit and create its environment file:

```bash
sudo install -D -m 0644 systemd/upcycle-monitor-exporter.service \
  /etc/systemd/system/upcycle-monitor-exporter.service
sudo install -D -m 0600 /dev/null /etc/upcycle-monitor/exporter.env
sudo systemctl daemon-reload
sudo systemctl enable --now upcycle-monitor-exporter
```

The service unit expects the exporter directory at
`/opt/upcycle-monitor/exporter`. If it is deployed elsewhere, update
`WorkingDirectory` and `ExecStart` in the unit before installing it.

The package installation is important: because this repository uses a `src`
layout, `monitor_exporter` is not importable from the repository root unless
it is installed into the interpreter used by systemd.
