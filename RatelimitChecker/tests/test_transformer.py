import pytest
from src.transformer import suggest_rate_limit


def get_base_config():
    return {
        "analysis": {
            "latency_threshold_ms": 200,
            "error_threshold_percent": 5
        },
        "rate_limit": {
            "base_limit_per_min": 50,
            "increase_step": 10,
            "decrease_step": 10,
            "min_limit_per_min": 20,
            "max_limit_per_min": 100
        }
    }


# Healthy system → increase rate
def test_healthy_system():
    config = get_base_config()
    calculations = {
        "avg_latency": 0.15,
        "error_rate": 0.02
    }

    result = suggest_rate_limit(calculations, config)

    assert result.system_status == "Healthy"
    assert result.suggested_rate_limit == 60
    assert "within acceptable" in result.reason


# High latency → decrease rate
def test_high_latency():
    config = get_base_config()
    calculations = {
        "avg_latency": 0.25,
        "error_rate": 0.02
    }

    result = suggest_rate_limit(calculations, config)

    assert result.system_status == "Unhealthy"
    assert result.suggested_rate_limit == 40
    assert "latency" in result.reason


# High error rate → decrease rate
def test_high_error_rate():
    config = get_base_config()
    calculations = {
        "avg_latency": 0.15,
        "error_rate": 0.08
    }

    result = suggest_rate_limit(calculations, config)

    assert result.system_status == "Unhealthy"
    assert result.suggested_rate_limit == 40
    assert "Error rate" in result.reason


#  Both high → decrease rate
def test_high_latency_and_error():
    config = get_base_config()
    calculations = {
        "avg_latency": 0.25,
        "error_rate": 0.08
    }

    result = suggest_rate_limit(calculations, config)

    assert result.system_status == "Unhealthy"
    assert result.suggested_rate_limit == 40
    assert "latency" in result.reason and "Error rate" in result.reason


#  Min rate boundary
def test_min_rate_enforced():
    config = get_base_config()
    config["rate_limit"]["base_limit_per_min"] = 25
    config["rate_limit"]["decrease_step"] = 10

    calculations = {
        "avg_latency": 0.25,
        "error_rate": 0.08
    }

    result = suggest_rate_limit(calculations, config)

    assert result.suggested_rate_limit == 20  # min limit


# Max rate boundary
def test_max_rate_enforced():
    config = get_base_config()
    config["rate_limit"]["base_limit_per_min"] = 95
    config["rate_limit"]["increase_step"] = 10

    calculations = {
        "avg_latency": 0.10,
        "error_rate": 0.01
    }

    result = suggest_rate_limit(calculations, config)

    assert result.suggested_rate_limit == 100  # max limit


#  Missing calculations
def test_no_calculations():
    config = get_base_config()

    result = suggest_rate_limit(None, config)

    assert result is None


# Missing config
def test_no_config():
    calculations = {
        "avg_latency": 0.2,
        "error_rate": 0.02
    }

    result = suggest_rate_limit(calculations, None)

    assert result is None