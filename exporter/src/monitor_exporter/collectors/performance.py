"""System performance collectors."""
from dataclasses import dataclass
import logging
import psutil
import time

# Collect CPU and RAM metrics here.


LOGGER = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics collected from the system."""

    timestamp: float
    cpu: dict
    memory: dict
    swap: dict
    host: dict

    @classmethod
    def collect(cls) -> "PerformanceMetrics":
        """Collect current system performance metrics."""
        LOGGER.debug("Collecting performance metrics")
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return cls(
            timestamp=time.time(),
            cpu={
                "usage_percent": psutil.cpu_percent(interval=None),
                "per_core_percent": psutil.cpu_percent(
                    interval=None, percpu=True
                ),
                "load_average": psutil.getloadavg(),
            },
            memory={
                "total_bytes": memory.total,
                "available_bytes": memory.available,
                "usage_percent": memory.percent,
            },
            swap={
                "total_bytes": swap.total,
                "used_bytes": swap.used,
                "usage_percent": swap.percent,
            },
            host={
                "boot_time": psutil.boot_time(),
                "logical_cpu_count": psutil.cpu_count(),
            },
        )