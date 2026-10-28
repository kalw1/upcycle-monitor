"""System power and battery collectors."""
from dataclasses import dataclass
import logging
from pathlib import Path

from ..config import CONFIG

# Collect battery percentage, charging state, AC connection here.


LOGGER = logging.getLogger(__name__)


def _read_string(path: Path) -> str | None:
    """Read a sysfs attribute, or return None if unavailable."""
    try:
        return path.read_text().strip()
    except OSError:
        LOGGER.debug("Unable to read power statistic at %s", path)
        return None

def _read_int(path: Path) -> int | None:
    """Read an integer sysfs attribute."""
    value = _read_string(path)

    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        LOGGER.warning("Invalid integer in power statistic at %s: %r", path, value)
        return None

def _read_bool(path: Path) -> bool | None:
    """Read a sysfs boolean represented by 0 or 1."""
    value = _read_string(path)

    if value == "1":
        return True
    if value == "0":
        return False

    return None

@dataclass
class BatteryMetrics:
    """Battery telemetry collected from the system."""

    capacity: int | None
    status: str | None
    present: bool | None
    capacity_level: str | None
    charge_now: int | None
    charge_full: int | None
    charge_full_design: int | None
    cycle_count: int | None
    current_now: int | None
    voltage_now: int | None
    voltage_min_design: int | None
    technology: str | None
    manufacturer: str | None
    model_name: str | None

    @classmethod
    def collect(cls) -> "BatteryMetrics":
        LOGGER.debug("Collecting battery metrics")
        paths = CONFIG.battery

        return cls(
            capacity=_read_int(paths.capacity),
            status=_read_string(paths.status),
            present=_read_bool(paths.present),
            capacity_level=_read_string(paths.capacity_level),
            charge_now=_read_int(paths.charge_now),
            charge_full=_read_int(paths.charge_full),
            charge_full_design=_read_int(paths.charge_full_design),
            cycle_count=_read_int(paths.cycle_count),
            current_now=_read_int(paths.current_now),
            voltage_now=_read_int(paths.voltage_now),
            voltage_min_design=_read_int(paths.voltage_min_design),
            technology=_read_string(paths.technology),
            manufacturer=_read_string(paths.manufacturer),
            model_name=_read_string(paths.model_name),
        )

@dataclass
class ACPowerMetrics:
    """External power connection telemetry."""

    online: bool | None

    @classmethod
    def collect(cls) -> "ACPowerMetrics":
        LOGGER.debug("Collecting AC power metrics")
        return cls(
            online=_read_bool(CONFIG.ac.online),
        )