"""Environment-backed configuration for the host exporter."""

from dataclasses import dataclass
import os
from pathlib import Path

POWER_SUPPLY_ROOT = Path(
    os.getenv("POWER_SUPPLY_ROOT", "/sys/class/power_supply")
)
BATTERY_FOLDER = os.getenv("BATTERY_FOLDER", "BAT1")
AC_FOLDER = os.getenv("AC_FOLDER", "ACAD")


def _get_file_env(variable: str, default: str) -> str:
    """Return a sysfs statistic filename, allowing device-specific overrides."""
    return os.getenv(variable, default)


def _battery_path(variable: str, default: str) -> Path:
    """Return the full path for a statistic on the configured battery."""
    return POWER_SUPPLY_ROOT / BATTERY_FOLDER / _get_file_env(variable, default)


def _ac_path(variable: str, default: str) -> Path:
    """Return the full path for a statistic on the configured AC adapter."""
    return POWER_SUPPLY_ROOT / AC_FOLDER / _get_file_env(variable, default)


@dataclass(frozen=True)
class BatteryPaths:
    """Full paths for statistics exposed by the configured battery device."""

    alarm: Path = _battery_path("BATTERY_ALARM_FILE", "alarm")
    capacity: Path = _battery_path("BATTERY_CAPACITY_FILE", "capacity")
    capacity_level: Path = _battery_path(
        "BATTERY_CAPACITY_LEVEL_FILE", "capacity_level"
    )
    charge_full: Path = _battery_path("BATTERY_CHARGE_FULL_FILE", "charge_full")
    charge_full_design: Path = _battery_path(
        "BATTERY_CHARGE_FULL_DESIGN_FILE", "charge_full_design"
    )
    charge_now: Path = _battery_path("BATTERY_CHARGE_NOW_FILE", "charge_now")
    cycle_count: Path = _battery_path("BATTERY_CYCLE_COUNT_FILE", "cycle_count")
    current_now: Path = _battery_path("BATTERY_CURRENT_NOW_FILE", "current_now")
    device: Path = _battery_path("BATTERY_DEVICE_FILE", "device")
    model_name: Path = _battery_path("BATTERY_MODEL_NAME_FILE", "model_name")
    manufacturer: Path = _battery_path(
        "BATTERY_MANUFACTURER_FILE", "manufacturer"
    )
    present: Path = _battery_path("BATTERY_PRESENT_FILE", "present")
    serial_number: Path = _battery_path(
        "BATTERY_SERIAL_NUMBER_FILE", "serial_number"
    )
    status: Path = _battery_path("BATTERY_STATUS_FILE", "status")
    subsystem: Path = _battery_path("BATTERY_SUBSYSTEM_FILE", "subsystem")
    technology: Path = _battery_path("BATTERY_TECHNOLOGY_FILE", "technology")
    type: Path = _battery_path("BATTERY_TYPE_FILE", "type")
    uevent: Path = _battery_path("BATTERY_UEVENT_FILE", "uevent")
    voltage_min_design: Path = _battery_path(
        "BATTERY_VOLTAGE_MIN_DESIGN_FILE", "voltage_min_design"
    )
    voltage_now: Path = _battery_path(
        "BATTERY_VOLTAGE_NOW_FILE", "voltage_now"
    )


@dataclass(frozen=True)
class AcPaths:
    """Full paths for statistics exposed by the configured AC adapter."""

    device: Path = _ac_path("AC_DEVICE_FILE", "device")
    extensions: Path = _ac_path("AC_EXTENSIONS_FILE", "extensions")
    hwmon: Path = _ac_path("AC_HWMON_FILE", "hwmon0")
    online: Path = _ac_path("AC_ONLINE_FILE", "online")
    power: Path = _ac_path("AC_POWER_FILE", "power")
    subsystem: Path = _ac_path("AC_SUBSYSTEM_FILE", "subsystem")
    type: Path = _ac_path("AC_TYPE_FILE", "type")
    uevent: Path = _ac_path("AC_UEVENT_FILE", "uevent")
    wakeup: Path = _ac_path("AC_WAKEUP_FILE", "wakeup19")


@dataclass(frozen=True)
class ExporterConfig:
    """Runtime settings shared by the exporter components."""

    backend_url: str = os.getenv("EXPORTER_BACKEND_URL", "http://localhost:8000")
    auth_token: str | None = os.getenv("EXPORTER_AUTH_TOKEN")
    collection_interval_seconds: float = max(0.1, float(
        os.getenv("EXPORTER_COLLECTION_INTERVAL_SECONDS", "30")
    ))
    battery: BatteryPaths = BatteryPaths()
    ac: AcPaths = AcPaths()

CONFIG = ExporterConfig()