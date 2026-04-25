from main import get_version
import subprocess


def test_get_version_returns_correct_value():
    assert get_version() == "0.0.1"


def test_cli_version_flag():
    result = subprocess.run(
        ["python", "main.py", "--version"], capture_output=True, text=True
    )

    assert result.stdout.strip() == "0.0.1"
