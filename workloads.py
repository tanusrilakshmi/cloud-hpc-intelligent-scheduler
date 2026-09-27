import numpy as np
import time


def matrix_multiplication(size):
    """
    Performs matrix multiplication and measures execution time.
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
import subprocess
import os


def run_openmp_matrix_multiplication(size, threads):
    """
    Run the compiled OpenMP matrix multiplication worker.
    """

    project_root = os.path.dirname(
        os.path.abspath(__file__)
    )

    worker_path = os.path.join(
        project_root,
        "workers",
        "openmp_worker.exe"
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
        raise RuntimeError(process.stderr)

    output = {}

    for line in process.stdout.strip().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            output[key] = value

    return {
        "workload": output["WORKLOAD"],
        "size": int(output["SIZE"]),
        "threads": int(output["THREADS"]),
        "execution_time": float(output["EXECUTION_TIME"]),
        "result_sample": float(output["RESULT_SAMPLE"])
    }
import subprocess
import os


def run_openmp_matrix_multiplication(size, threads):
    """
    Run the compiled OpenMP matrix multiplication worker.
    """

    project_root = os.path.dirname(
        os.path.abspath(__file__)
    )

    worker_path = os.path.join(
        project_root,
        "workers",
        "openmp_worker.exe"
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
        raise RuntimeError(process.stderr)

    output = {}

    for line in process.stdout.strip().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            output[key] = value

    return {
        "workload": output["WORKLOAD"],
        "size": int(output["SIZE"]),
        "threads": int(output["THREADS"]),
        "execution_time": float(output["EXECUTION_TIME"]),
        "result_sample": float(output["RESULT_SAMPLE"])
    }