def suggest_rate_limit(calculations, config):
    if calculations is None:
        print("No calculations provided for rate limit suggestion.")
        return 
    elif config is None:
        print("No configuration provided for rate limit suggestion.")
        return

    latency_threshold = config["analysis"]["latency_threshold_ms"]
    error_threshold_percent = config["analysis"]["error_threshold_percent"]
    base_rate = config["rate_limit"]["base_limit_per_min"]
    increase_rate = config["rate_limit"]["increase_step"]
    decrease_rate = config["rate_limit"]["decrease_step"]

    raw_avg_latency = calculations.get("avg_latency")
    raw_error_rate = calculations.get("error_rate")

    if raw_avg_latency is None:
        return{
            "system_status" : "Unhealthy",
            "reason" : "Average latency is not available in calculations."
        }
    if raw_error_rate is None:
        return{
            "system_status" : "Unhealthy",
            "reason" : "Error rate is not available in calculations."
        }

    avg_latency = raw_avg_latency * 1000
    error_rate = raw_error_rate * 100

    system_status = ""
    min_rate = config["rate_limit"]["min_limit_per_min"]
    max_rate = config["rate_limit"]["max_limit_per_min"]
    reason = ""
    is_latency_high = avg_latency > latency_threshold
    is_error_high = error_rate > error_threshold_percent

    if is_latency_high or is_error_high:
        system_status = "Unhealthy"
        base_rate = base_rate - decrease_rate
        if base_rate < min_rate:
            base_rate = min_rate
        if is_latency_high and not is_error_high:
            reason = f"Average latency ({avg_latency:.2f} ms) exceeds threshold ({latency_threshold} ms)" 
        elif is_error_high and not is_latency_high:
            reason = f"Error rate ({error_rate:.2f}%) exceeds threshold ({error_threshold_percent}%)"
        elif is_latency_high and is_error_high:
            reason = f"Average latency ({avg_latency:.2f} ms) and Error rate ({error_rate:.2f}%) are above thresholds ({latency_threshold} ms and {error_threshold_percent}%) respectively"
        return{
            "system_status": system_status,
            "suggested_rate_limit": base_rate,
            "reason": reason
        }
    else:
        system_status = "Healthy"
        base_rate = base_rate + increase_rate
        if base_rate > max_rate:
            base_rate = max_rate
        return{
            "system_status": system_status,
            "suggested_rate_limit": base_rate,
            "reason": f"Average latency is ({avg_latency:.2f} ms) and error rate is ({error_rate:.2f}%). Both are within acceptable thresholds."
        }