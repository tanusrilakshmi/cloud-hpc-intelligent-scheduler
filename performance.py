def calculate_speedup(serial_time, parallel_time):
    """Calculate speedup."""
    if parallel_time <= 0:
        return 0

    return serial_time / parallel_time


def calculate_efficiency(speedup, workers):
    """Calculate parallel efficiency."""
    if workers <= 0:
        return 0

    return (speedup / workers) * 100


def create_performance_report(
    serial_time,
    parallel_time,
    workers
):
    """Create a performance summary."""

    speedup = calculate_speedup(
        serial_time,
        parallel_time
    )

    efficiency = calculate_efficiency(
        speedup,
        workers
    )

    return {
        "serial_time": serial_time,
        "parallel_time": parallel_time,
        "workers": workers,
        "speedup": speedup,
        "efficiency": efficiency
    }