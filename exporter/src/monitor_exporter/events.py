"""Metric payload construction and delivery to the backend."""

from dataclasses import asdict
import logging
from typing import Any

import requests

from .collectors.performance import PerformanceMetrics
from .collectors.power import ACPowerMetrics, BatteryMetrics
from .config import CONFIG


LOGGER = logging.getLogger(__name__)


def build_metrics_payload(
    battery: BatteryMetrics,
    ac: ACPowerMetrics,
    performance: PerformanceMetrics,
) -> dict[str, Any]:
    """Convert collected metric objects into the backend request shape."""
    return {
        "battery": asdict(battery),
        "ac": asdict(ac),
        "performance": asdict(performance),
    }


def send_metrics_to_backend(
    battery: BatteryMetrics,
    ac: ACPowerMetrics,
    performance: PerformanceMetrics,
) -> requests.Response:
    """Send collected metrics and raise an error when delivery fails."""
    headers: dict[str, str] = {}
    if CONFIG.auth_token:
        headers["Authorization"] = "Bearer " + CONFIG.auth_token

    endpoint = f"{CONFIG.backend_url.rstrip('/')}/metrics"
    LOGGER.debug("Submitting metrics to %s", endpoint)
    response = requests.post(
        endpoint,
        json=build_metrics_payload(battery, ac, performance),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response
