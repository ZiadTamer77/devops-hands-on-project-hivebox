"""Test Module for Main Application"""

from app.services.version_service import get_version


def test_get_version_returns_correct_value():
    """Test that get_version returns the correct version string"""
    assert get_version() == "0.0.1"
