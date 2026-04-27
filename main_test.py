"""Test Module for Main Application"""

import subprocess
from main import get_version


def test_get_version_returns_correct_value():
    """Test that get_version returns the correct version string"""
    assert get_version() == "0.0.1"


def test_cli_version_flag():
    """Test that the CLI version flag prints the correct version"""
    result = subprocess.run(
        ["python", "main.py", "--version"], capture_output=True, text=True, check=True
    )

    assert result.stdout.strip() == "0.0.1"
