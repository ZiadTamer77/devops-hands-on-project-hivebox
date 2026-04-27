
"""Unit tests for temperature_service — all HTTP is mocked."""

from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import pytest

from app.services.temperature_service import get_average_temperature


def make_box(temp_value, minutes_ago):
    """
    Helper: builds a fake senseBox dict with one temperature sensor.
    minutes_ago controls how old the measurement is.
    """
    timestamp = (
        datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    ).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return {
        "sensors": [
            {
                "title": "Temperatur",
                "lastMeasurement": {
                    "value": str(temp_value),
                    "createdAt": timestamp,
                },
            }
        ]
    }


def make_box_no_measurement():
    """Helper: builds a senseBox with a sensor but no lastMeasurement."""
    return {
        "sensors": [
            {
                "title": "Temperatur",
                "lastMeasurement": None,
            }
        ]
    }


# ── Test 1 ───────────────────────────────────────────────────────────────────
def test_returns_correct_average_for_fresh_boxes():
    """
    Given two boxes with fresh data (30 min old),
    the service should return the correct average and box count.
    """
    fake_boxes = [
        make_box(20.0, minutes_ago=30),
        make_box(30.0, minutes_ago=30),
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_boxes

    with patch("app.services.temperature_service.requests.get", return_value=mock_response):
        result = get_average_temperature()

    assert result["average_temperature"] == 25.0
    assert result["unit"] == "°C"
    assert result["box_count"] == 2


# ── Test 2 ───────────────────────────────────────────────────────────────────
def test_excludes_stale_boxes_from_average():
    """
    Given one fresh box (30 min) and one stale box (90 min),
    only the fresh box should contribute to the average.
    """
    fake_boxes = [
        make_box(20.0, minutes_ago=30),   # fresh
        make_box(100.0, minutes_ago=90),  # stale — must be excluded
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_boxes

    with patch("app.services.temperature_service.requests.get", return_value=mock_response):
        result = get_average_temperature()

    assert result["average_temperature"] == 20.0
    assert result["box_count"] == 1


# ── Test 3 ───────────────────────────────────────────────────────────────────
def test_returns_none_when_all_boxes_are_stale():
    """
    Given all boxes with measurements older than 1 hour,
    the service should return None to signal no fresh data.
    """
    fake_boxes = [
        make_box(20.0, minutes_ago=120),
        make_box(25.0, minutes_ago=90),
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_boxes

    with patch("app.services.temperature_service.requests.get", return_value=mock_response):
        result = get_average_temperature()

    assert result is None


# ── Test 4 ───────────────────────────────────────────────────────────────────
def test_raises_runtime_error_on_non_200_response():
    """
    If OpenSenseMap returns a non-200 status,
    the service should raise a RuntimeError.
    """
    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("app.services.temperature_service.requests.get", return_value=mock_response):
        with pytest.raises(RuntimeError):
            get_average_temperature()


# ── Test 5 ───────────────────────────────────────────────────────────────────
def test_raises_connection_error_when_api_unreachable():
    """
    If the HTTP call itself fails (network error),
    the service should raise a ConnectionError.
    """
    import requests as req

    with patch(
        "app.services.temperature_service.requests.get",
        side_effect=req.exceptions.ConnectionError,
    ):
        with pytest.raises(ConnectionError):
            get_average_temperature()


# ── Test 6 ───────────────────────────────────────────────────────────────────
def test_ignores_sensors_with_no_measurement():
    """
    If a box has a temperature sensor but lastMeasurement is None,
    that box should be skipped gracefully.
    """
    fake_boxes = [
        make_box_no_measurement(),
        make_box(22.0, minutes_ago=10),
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_boxes

    with patch("app.services.temperature_service.requests.get", return_value=mock_response):
        result = get_average_temperature()

    assert result["average_temperature"] == 22.0
    assert result["box_count"] == 1