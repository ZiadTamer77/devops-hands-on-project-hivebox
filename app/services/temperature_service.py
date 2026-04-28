import requests
from datetime import datetime, timezone, timedelta

from app.config.sensebox import OPENSENSEMAP_BASE_URL

STALE_THRESHOLD_MINUTES = 60


def _is_fresh(created_at_str):
    """
    Returns True if the timestamp is within the last hour.
    Timestamp format from OpenSenseMap: "2024-01-01T12:00:00.000Z"
    """
    measurement_time = datetime.strptime(
        created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ"
    ).replace(tzinfo=timezone.utc)

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=STALE_THRESHOLD_MINUTES)

    return measurement_time >= cutoff


def _find_temperature_sensor(box):
    """
    Returns the first sensor whose title contains 'temp' (case-insensitive).
    Returns None if no such sensor exists.
    """
    for sensor in box.get("sensors", []):
        if "temp" in sensor.get("title", "").lower():
            return sensor
    return None


def get_average_temperature():
    """
    Fetches all senseBoxes with temperature sensors from OpenSenseMap,
    filters out stale measurements (older than 1 hour),
    and returns the average temperature with metadata.

    Returns:
        dict with average_temperature, unit, box_count — if fresh data exists
        None — if all data is stale or no valid readings found

    Raises:
        ConnectionError — if OpenSenseMap is unreachable
        RuntimeError   — if OpenSenseMap returns a non-200 response
    """
    url = f"{OPENSENSEMAP_BASE_URL}/boxes?phenomenon=temperature"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("OpenSenseMap API is unreachable")

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenSenseMap returned unexpected status: {response.status_code}"
        )

    boxes = response.json()
    fresh_readings = []

    for box in boxes:
        sensor = _find_temperature_sensor(box)

        if sensor is None:
            continue

        measurement = sensor.get("lastMeasurement")
        if measurement is None:
            continue

        if not _is_fresh(measurement["createdAt"]):
            continue

        try:
            fresh_readings.append(float(measurement["value"]))
        except (ValueError, TypeError):
            continue

    if not fresh_readings:
        return None

    average = round(sum(fresh_readings) / len(fresh_readings), 2)

    return {
        "average_temperature": average,
        "unit": "°C",
        "box_count": len(fresh_readings),
    }