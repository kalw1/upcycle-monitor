"""Host exporter entry point."""

import logging
import os
import time

import requests

from .collectors.performance import PerformanceMetrics
from .collectors.power import ACPowerMetrics, BatteryMetrics
from .config import CONFIG
from .events import send_metrics_to_backend


LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure exporter logs for systemd or interactive execution."""
    level_name = os.getenv("EXPORTER_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid EXPORTER_LOG_LEVEL: {level_name}")

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def run_once() -> None:
    """Collect and send one snapshot of exporter metrics."""
    battery = BatteryMetrics.collect()
    ac = ACPowerMetrics.collect()
    performance = PerformanceMetrics.collect()

    send_metrics_to_backend(battery, ac, performance)
    LOGGER.info("Submitted metrics to %s", CONFIG.backend_url)


def run() -> None:
    """Run the exporter in a loop, collecting and sending metrics."""
    configure_logging()
    LOGGER.info(
        "Starting exporter with a %s-second collection interval",
        CONFIG.collection_interval_seconds,
    )

    try:
        while True:
            try:
                run_once()
            except (OSError, requests.RequestException, ValueError):
                LOGGER.exception("Metric collection or submission failed")
            time.sleep(CONFIG.collection_interval_seconds)
    except KeyboardInterrupt:
        LOGGER.info("Exporter stopped")