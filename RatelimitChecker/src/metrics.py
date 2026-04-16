from dataclasses import dataclass
from flask import logging

@dataclass
class MetricResults:
    total_requests: int
    successful_requests: int
    error_requests: int
    max_latency: float | None
    avg_latency: float
    error_rate: float

def calculate_metrics(request_results: list[dict]) -> MetricResults:
    total_requests = 0
    successful_requests = 0
    max_latency = None
    total_latency = 0
    valid_latency_count = 0
    error_requests = 0

    for request in request_results: 
        status_code = request.get("status_code") if request is not None else None
        response_time = request.get("response_time") if request is not None else None 
        if request is not None:
            total_requests += 1
            if status_code is not None:
                if  (200 <= status_code < 300):
                    successful_requests += 1
                else:
                    error_requests += 1
            else:
                error_requests += 1
            if  response_time is not None:
                max_latency = response_time if max_latency is None else max(max_latency, response_time)
                total_latency += response_time
                valid_latency_count += 1

    avg_latency = total_latency / valid_latency_count if valid_latency_count > 0 else 0

    error_rate = error_requests / total_requests if total_requests > 0 else 0

    return MetricResults(
        total_requests=total_requests,
        successful_requests=successful_requests,
        error_requests=error_requests,
        max_latency=max_latency,
        avg_latency=avg_latency,
        error_rate=error_rate
    )
