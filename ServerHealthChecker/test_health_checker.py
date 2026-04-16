import pytest
import json
import os
from unittest.mock import patch, MagicMock

from utils import load_json
from checkers import check_server
from main import HealthCheck

def test_load_config_file_not_found():
    config = load_json("non_existent_config.json")
    assert config is None

def test_load_config_invalid_json(tmp_path):
    bad_file = tmp_path / "bad_config.json"
    bad_file.write_text("{invalid_json: }")  # broken JSON
    with pytest.raises(json.JSONDecodeError):
        load_json(str(bad_file))

@patch("checkers.requests.get")
def test_check_server_http_up(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    server = {
        "name": "test-http",
        "type": "http",
        "target": "http://example.com"
    }

    result = check_server(server, timeout=2)
    assert result is True

@patch("checkers.subprocess.run")
def test_check_server_ping_down(mock_run):
    mock_run.return_value.returncode = 1  # failure

    server = {
        "name": "test-ping",
        "type": "ping",
        "target": "192.0.2.1"
    }

    result = check_server(server, timeout=2)
    assert result is False

def test_generate_report_mixed_results():
    config = {
        "servers": [
            {"name": "s1", "type": "http", "target": "a"},
            {"name": "s2", "type": "http", "target": "b"},
            {"name": "s3", "type": "http", "target": "c"}
        ],
        "timeout": 2
    }

    checker = HealthCheck(config)

    # Inject fake results directly (don’t depend on real network)
    checker.results = [
        ("s1", True),
        ("s2", False),
        ("s3", True)
    ]

    # Capture printed output
    from io import StringIO
    import sys

    captured_output = StringIO()
    sys.stdout = captured_output

    checker.generate_report()

    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "UP: 2" in output
    assert "DOWN: 1" in output

