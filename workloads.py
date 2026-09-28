import numpy as np
import time
import subprocess
import os


def matrix_multiplication(size):
    """
    Performs matrix multiplication using NumPy
    and measures execution time.
    """

    np.random.seed(42)

    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)

    start_time = time.perf_counter()

    result = np.matmul(matrix_a, matrix_b)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return {
        "workload": "Matrix Multiplication",
        "size": size,
        "execution_time": execution_time,
        "result_shape": result.shape
    }


def run_openmp_matrix_multiplication(size, threads):
    """
    Runs the compiled OpenMP matrix multiplication worker.

    Uses:
        openmp_worker.exe  -> Windows
        openmp_worker      -> Linux/Azure
    """

    project_root = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Select the correct executable for the operating system
    if os.name == "nt":
        worker_name = "openmp_worker.exe"
    else:
        worker_name = "openmp_worker"

    worker_path = os.path.join(
        project_root,
        "workers",
        worker_name
    )

    # Make sure the worker exists
    if not os.path.isfile(worker_path):
        raise FileNotFoundError(
            f"OpenMP worker not found: {worker_path}"
        )

    command = [
        worker_path,
        str(size),
        str(threads)
    ]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if process.returncode != 0:
        error_message = process.stderr.strip()

        if not error_message:
            error_message = "OpenMP worker execution failed."

        raise RuntimeError(error_message)

    output = {}

    for line in process.stdout.strip().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            output[key] = value

    # Validate required worker output
    required_keys = [
        "WORKLOAD",
        "SIZE",
        "THREADS",
        "EXECUTION_TIME",
        "RESULT_SAMPLE"
    ]

    for key in required_keys:
        if key not in output:
            raise RuntimeError(
                f"OpenMP worker returned incomplete output. "
                f"Missing: {key}"
            )

    return {
        "workload": output["WORKLOAD"],
        "size": int(output["SIZE"]),
        "threads": int(output["THREADS"]),
        "execution_time": float(output["EXECUTION_TIME"]),
        "result_sample": float(output["RESULT_SAMPLE"])
    }
