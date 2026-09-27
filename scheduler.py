import os


def schedule_workload(size, priority):
    """
    Intelligent workload scheduler.

    Selects an appropriate number of CPU threads
    based on workload size, job priority, and
    available CPU resources.
    """

    cpu_count = os.cpu_count() or 1

    # Keep the scheduler within a safe limit
    max_workers = min(cpu_count, 4)

    if priority == "High":
        workers = max_workers
        strategy = "High-priority workload - maximum parallelism"

    elif size >= 1000:
        workers = max_workers
        strategy = "Large workload - maximum parallelism"

    elif size >= 500:
        workers = min(2, max_workers)
        strategy = "Medium workload - moderate parallelism"

    else:
        workers = 1
        strategy = "Small workload - single worker"

    return {
        "workers": workers,
        "strategy": strategy,
        "workload_size": size,
        "priority": priority,
        "available_cpu_threads": cpu_count
    }