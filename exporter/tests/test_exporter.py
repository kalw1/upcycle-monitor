"""Tests for the host exporter."""

from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock, patch

from monitor_exporter import config
from monitor_exporter.collectors import performance, power
from monitor_exporter.events import build_metrics_payload, send_metrics_to_backend


def test_config_builds_full_statistic_paths():
    assert config.CONFIG.battery.status == Path(
        "/sys/class/power_supply/BAT1/status"
    )
    assert config.CONFIG.ac.online == Path(
        "/sys/class/power_supply/ACAD/online"
    )


def test_battery_collection_reads_sysfs_values(tmp_path):
    values = {
        "capacity": "87\n",
        "status": "Charging\n",
        "present": "1\n",
        "capacity_level": "Normal\n",
        "charge_now": "4200\n",
        "charge_full": "5000\n",
        "charge_full_design": "5500\n",
        "cycle_count": "12\n",
        "current_now": "900\n",
        "voltage_now": "12000\n",
        "voltage_min_design": "9000\n",
        "technology": "Li-ion\n",
        "manufacturer": "Example\n",
        "model_name": "Battery\n",
    }
    for filename, value in values.items():
        (tmp_path / filename).write_text(value)

    paths = replace(
        config.CONFIG.battery,
        **{name: tmp_path / name for name in values},
    )
    with patch.object(power, "CONFIG", replace(config.CONFIG, battery=paths)):
        metrics = power.BatteryMetrics.collect()

    assert metrics.capacity == 87
    assert metrics.status == "Charging"
    assert metrics.present is True
    assert metrics.charge_full == 5000


def test_ac_collection_converts_online_flag(tmp_path):
    online = tmp_path / "online"
    online.write_text("0\n")
    paths = replace(config.CONFIG.ac, online=online)

    with patch.object(power, "CONFIG", replace(config.CONFIG, ac=paths)):
        metrics = power.ACPowerMetrics.collect()

    assert metrics.online is False


def test_performance_collection_uses_system_metrics():
    with (
        patch.object(performance.psutil, "virtual_memory") as virtual_memory,
        patch.object(performance.psutil, "swap_memory") as swap_memory,
        patch.object(
            performance.psutil,
            "cpu_percent",
            side_effect=[25.0, [20.0, 30.0]],
        ),
        patch.object(
            performance.psutil,
            "getloadavg",
            return_value=(1.0, 0.5, 0.25),
        ),
        patch.object(performance.psutil, "boot_time", return_value=100.0),
        patch.object(performance.psutil, "cpu_count", return_value=2),
    ):
        virtual_memory.return_value = Mock(
            total=1000,
            available=400,
            percent=60.0,
        )
        swap_memory.return_value = Mock(total=2000, used=500, percent=25.0)

        metrics = performance.PerformanceMetrics.collect()

    assert metrics.cpu["usage_percent"] == 25.0
    assert metrics.cpu["per_core_percent"] == [20.0, 30.0]
    assert metrics.memory["usage_percent"] == 60.0
    assert metrics.swap["used_bytes"] == 500
    assert metrics.host["logical_cpu_count"] == 2


def test_build_metrics_payload_serializes_dataclasses():
    battery = power.BatteryMetrics(
        capacity=80,
        status="Discharging",
        present=True,
        capacity_level="Normal",
        charge_now=4000,
        charge_full=5000,
        charge_full_design=5500,
        cycle_count=12,
        current_now=900,
        voltage_now=12000,
        voltage_min_design=9000,
        technology="Li-ion",
        manufacturer="Example",
        model_name="Battery",
    )
    ac = power.ACPowerMetrics(online=True)
    performance_metrics = performance.PerformanceMetrics(
        timestamp=1.0,
        cpu={"usage_percent": 20.0},
        memory={},
        swap={},
        host={},
    )

    payload = build_metrics_payload(battery, ac, performance_metrics)

    assert payload["battery"]["capacity"] == 80
    assert payload["ac"]["online"] is True
    assert payload["performance"]["timestamp"] == 1.0


def test_send_metrics_uses_bearer_auth_and_endpoint():
    response = Mock()
    exporter_config = replace(
        config.CONFIG,
        backend_url="http://backend:8000/",
        auth_token="test-token",
    )
    battery = Mock()
    ac = Mock()
    performance_metrics = Mock()

    with (
        patch("monitor_exporter.events.CONFIG", exporter_config),
        patch(
            "monitor_exporter.events.build_metrics_payload",
            return_value={"ok": True},
        ),
        patch(
            "monitor_exporter.events.requests.post",
            return_value=response,
        ) as post,
    ):
        result = send_metrics_to_backend(
            battery,
            ac,
            performance_metrics,
        )

    assert result is response
    post.assert_called_once_with(
        "http://backend:8000/metrics",
        json={"ok": True},
        headers={"Authorization": "Bearer " + "test-" + "token"},
        timeout=10,
    )
    response.raise_for_status.assert_called_once_with()


def test_send_metrics_propagates_backend_failure():
    response = Mock()
    response.raise_for_status.side_effect = RuntimeError("backend rejected payload")

    with (
        patch(
            "monitor_exporter.events.build_metrics_payload",
            return_value={"ok": True},
        ),
        patch("monitor_exporter.events.requests.post", return_value=response),
    ):
        try:
            send_metrics_to_backend(Mock(), Mock(), Mock())
        except RuntimeError as error:
            assert str(error) == "backend rejected payload"
        else:
            raise AssertionError("backend failure was swallowed")
