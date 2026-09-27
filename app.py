import os
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from workloads import run_openmp_matrix_multiplication
from scheduler import schedule_workload
from performance import create_performance_report


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cloud HPC Intelligent Workload Scheduler",
    page_icon="⚡",
    layout="wide"
)

HISTORY_FILE = os.path.join(
    "results",
    "job_history.csv"
)


# ============================================================
# HISTORY FUNCTIONS
# ============================================================

def load_history():
    """Load completed job history."""

    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()

    try:
        history = pd.read_csv(HISTORY_FILE)

        # Prevent Streamlit/PyArrow mixed-type problems
        if not history.empty:
            history["Job ID"] = history["Job ID"].astype(str)
            history["Timestamp"] = history["Timestamp"].astype(str)
            history["Workload"] = history["Workload"].astype(str)
            history["Priority"] = history["Priority"].astype(str)
            history["Strategy"] = history["Strategy"].astype(str)
            history["Status"] = history["Status"].astype(str)

        return history

    except Exception:
        return pd.DataFrame()


def save_job(job):
    """Save a completed job to CSV."""

    columns = [
        "Job ID",
        "Timestamp",
        "Workload",
        "Matrix Size",
        "Priority",
        "Threads Allocated",
        "Available CPU Threads",
        "Single-Thread Time",
        "Parallel Time",
        "Speedup",
        "Parallel Efficiency %",
        "Strategy",
        "Status"
    ]

    new_row = pd.DataFrame(
        [job],
        columns=columns
    )

    if os.path.exists(HISTORY_FILE):

        try:
            existing = pd.read_csv(
                HISTORY_FILE
            )

            combined = pd.concat(
                [existing, new_row],
                ignore_index=True
            )

        except Exception:

            combined = new_row

    else:

        combined = new_row

    combined.to_csv(
        HISTORY_FILE,
        index=False
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "⚡ Cloud-Based Intelligent Workload Scheduler"
)

st.subheader(
    "AI and High-Performance Computing Workload Management System"
)

st.write(
    "The system analyzes a computational workload, "
    "selects an execution strategy, allocates CPU threads "
    "using the intelligent scheduler, and executes the "
    "workload using OpenMP parallel computing."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Job Configuration"
)

workload_type = st.sidebar.selectbox(
    "Workload Type",
    [
        "Matrix Multiplication"
    ]
)

matrix_size = st.sidebar.selectbox(
    "Matrix Size",
    [
        200,
        500,
        750,
        1000,
        1500
    ]
)

priority = st.sidebar.selectbox(
    "Job Priority",
    [
        "Low",
        "Medium",
        "High"
    ]
)


# ============================================================
# JOB INFORMATION
# ============================================================

st.header(
    "📋 Job Information"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Workload",
        workload_type
    )

with col2:

    st.metric(
        "Matrix Size",
        f"{matrix_size} × {matrix_size}"
    )

with col3:

    st.metric(
        "Priority",
        priority
    )


# ============================================================
# SUBMIT WORKLOAD
# ============================================================

submit = st.button(
    "🚀 Submit Workload",
    use_container_width=True
)


if submit:

    try:

        # ----------------------------------------------------
        # CREATE JOB ID
        # ----------------------------------------------------

        job_id = (
            "JOB-"
            + datetime.now().strftime("%Y%m%d-%H%M%S")
            + "-"
            + str(uuid.uuid4())[:4].upper()
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ----------------------------------------------------
        # AVAILABLE CPU
        # ----------------------------------------------------

        available_cpu = os.cpu_count()

        if available_cpu is None:
            available_cpu = 1


        # ----------------------------------------------------
        # INTELLIGENT SCHEDULER
        # ----------------------------------------------------

        scheduling_decision = schedule_workload(
            matrix_size,
            priority
        )

        requested_workers = scheduling_decision[
            "workers"
        ]

        workers = min(
            requested_workers,
            available_cpu
        )

        strategy = scheduling_decision[
            "strategy"
        ]


        # ----------------------------------------------------
        # SCHEDULER DECISION
        # ----------------------------------------------------

        st.header(
            "🧠 Intelligent Scheduler Decision"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "CPU Threads Allocated",
                workers
            )

        with col2:

            st.info(
                strategy
            )

        with col3:

            st.metric(
                "Available CPU Threads",
                available_cpu
            )


        # ----------------------------------------------------
        # EXECUTION
        # ----------------------------------------------------

        st.header(
            "⚙️ Workload Execution"
        )

        progress = st.progress(0)

        status = st.empty()

        status.write(
            "Preparing workload..."
        )

        progress.progress(20)


        status.write(
            "Allocating CPU resources..."
        )

        progress.progress(40)


        status.write(
            "Running single-thread baseline..."
        )

        progress.progress(50)


        # ----------------------------------------------------
        # SINGLE THREAD BASELINE
        # ----------------------------------------------------

        baseline_result = (
            run_openmp_matrix_multiplication(
                matrix_size,
                1
            )
        )

        single_thread_time = (
            baseline_result["execution_time"]
        )


        # ----------------------------------------------------
        # PARALLEL EXECUTION
        # ----------------------------------------------------

        status.write(
            f"Running OpenMP with {workers} threads..."
        )

        progress.progress(70)


        parallel_result = (
            run_openmp_matrix_multiplication(
                matrix_size,
                workers
            )
        )

        parallel_time = (
            parallel_result["execution_time"]
        )


        progress.progress(100)

        status.success(
            "Workload completed successfully "
            "using real OpenMP parallel execution."
        )


        # ----------------------------------------------------
        # PERFORMANCE CALCULATION
        # ----------------------------------------------------

        performance = create_performance_report(
            single_thread_time,
            parallel_time,
            workers
        )

        speedup = performance[
            "speedup"
        ]

        efficiency = performance[
            "efficiency"
        ]


        # ----------------------------------------------------
        # PERFORMANCE MEASUREMENT
        # ----------------------------------------------------

        st.header(
            "⏱️ Performance Measurement"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Single-Thread Time",
                f"{single_thread_time:.6f} sec"
            )

        with col2:

            st.metric(
                "Parallel Time",
                f"{parallel_time:.6f} sec"
            )

        with col3:

            st.metric(
                "Speedup",
                f"{speedup:.2f}×"
            )

        with col4:

            st.metric(
                "Parallel Efficiency",
                f"{efficiency:.2f}%"
            )


        # ----------------------------------------------------
        # PERFORMANCE CHART
        # ----------------------------------------------------

        st.header(
            "📊 Execution Time Comparison"
        )

        chart_data = pd.DataFrame(
            {
                "Execution Type": [
                    "Single Thread",
                    "OpenMP Parallel"
                ],
                "Execution Time (sec)": [
                    single_thread_time,
                    parallel_time
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index(
                "Execution Type"
            )
        )


        # ----------------------------------------------------
        # WORKLOAD EXECUTION DETAILS
        # ----------------------------------------------------

        st.header(
            "⚙️ Workload Execution Details"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Matrix Size",
                f"{matrix_size} × {matrix_size}"
            )

        with col2:

            st.metric(
                "OpenMP Threads",
                workers
            )

        with col3:

            st.metric(
                "Result Validation",
                "Successful"
            )


        # ----------------------------------------------------
        # JOB SUMMARY
        # ----------------------------------------------------

        st.header(
            "📌 Job Summary"
        )

        summary = pd.DataFrame(
            {
                "Parameter": [
                    "Job ID",
                    "Timestamp",
                    "Workload",
                    "Matrix Size",
                    "Priority",
                    "Scheduling Strategy",
                    "Threads Allocated",
                    "Available CPU Threads",
                    "Single-Thread Time",
                    "Parallel Time",
                    "Speedup",
                    "Parallel Efficiency",
                    "Execution Status"
                ],

                "Value": [
                    job_id,
                    timestamp,
                    workload_type,
                    f"{matrix_size} × {matrix_size}",
                    priority,
                    strategy,
                    workers,
                    available_cpu,
                    f"{single_thread_time:.6f} seconds",
                    f"{parallel_time:.6f} seconds",
                    f"{speedup:.2f}×",
                    f"{efficiency:.2f}%",
                    "Completed Successfully"
                ]
            }
        )

        st.table(
            summary
        )


        # ----------------------------------------------------
        # TECHNICAL EXECUTION DETAILS
        # ----------------------------------------------------

        st.header(
            "🔍 Technical Execution Details"
        )

        st.write(
            f"**Job ID:** {job_id}"
        )

        st.write(
            f"**Scheduler Decision:** {strategy}"
        )

        st.write(
            f"**CPU Threads Allocated:** {workers}"
        )

        st.write(
            f"**Available CPU Threads:** {available_cpu}"
        )

        st.write(
            f"**Parallel Framework:** OpenMP"
        )

        st.write(
            f"**Workload:** {workload_type}"
        )

        st.write(
            f"**Matrix Dimensions:** "
            f"{matrix_size} × {matrix_size}"
        )

        st.write(
            f"**Baseline Execution:** "
            f"1 CPU thread"
        )

        st.write(
            f"**Parallel Execution:** "
            f"{workers} CPU thread(s)"
        )

        st.write(
            f"**Speedup:** {speedup:.2f}×"
        )

        st.write(
            f"**Parallel Efficiency:** "
            f"{efficiency:.2f}%"
        )

        st.write(
            "**Execution Status:** Successful"
        )


        # ----------------------------------------------------
        # SAVE JOB
        # ----------------------------------------------------

        job = {

            "Job ID": job_id,

            "Timestamp": timestamp,

            "Workload": workload_type,

            "Matrix Size": matrix_size,

            "Priority": priority,

            "Threads Allocated": workers,

            "Available CPU Threads": available_cpu,

            "Single-Thread Time": single_thread_time,

            "Parallel Time": parallel_time,

            "Speedup": speedup,

            "Parallel Efficiency %": efficiency,

            "Strategy": strategy,

            "Status": "Successful"
        }

        save_job(job)


        st.success(
            f"✅ Job {job_id} has been saved "
            "to the workload history."
        )


    except Exception as error:

        st.error(
            "❌ Workload execution failed."
        )

        st.exception(error)


# ============================================================
# JOB HISTORY
# ============================================================

st.divider()

st.header(
    "🗂️ Job History"
)

history = load_history()


if history.empty:

    st.info(
        "No completed jobs have been recorded yet. "
        "Submit a workload to create the first history entry."
    )

else:

    # --------------------------------------------------------
    # HISTORY METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Jobs",
            len(history)
        )

    with col2:

        average_speedup = pd.to_numeric(
            history["Speedup"],
            errors="coerce"
        ).mean()

        st.metric(
            "Average Speedup",
            f"{average_speedup:.2f}×"
        )

    with col3:

        average_time = pd.to_numeric(
            history["Parallel Time"],
            errors="coerce"
        ).mean()

        st.metric(
            "Average Parallel Time",
            f"{average_time:.4f} sec"
        )

    with col4:

        average_efficiency = pd.to_numeric(
            history["Parallel Efficiency %"],
            errors="coerce"
        ).mean()

        st.metric(
            "Average Efficiency",
            f"{average_efficiency:.2f}%"
        )


    # --------------------------------------------------------
    # COMPLETED JOBS
    # --------------------------------------------------------

    st.subheader(
        "📋 Completed Jobs"
    )

    # Convert everything to string for safe Streamlit display
    display_history = history.copy()

    display_history = display_history.astype(
        str
    )

    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # SPEEDUP CHART
    # --------------------------------------------------------

    st.subheader(
        "📈 Speedup Across Jobs"
    )

    speedup_history = history.copy()

    speedup_history[
        "Speedup"
    ] = pd.to_numeric(
        speedup_history["Speedup"],
        errors="coerce"
    )

    speedup_history[
        "Job"
    ] = range(
        1,
        len(speedup_history) + 1
    )

    st.line_chart(
        speedup_history.set_index(
            "Job"
        )["Speedup"]
    )


    # --------------------------------------------------------
    # THREAD ALLOCATION CHART
    # --------------------------------------------------------

    st.subheader(
        "🧵 CPU Thread Allocation"
    )

    thread_history = history.copy()

    thread_history[
        "Threads Allocated"
    ] = pd.to_numeric(
        thread_history[
            "Threads Allocated"
        ],
        errors="coerce"
    )

    thread_history[
        "Job"
    ] = range(
        1,
        len(thread_history) + 1
    )

    st.bar_chart(
        thread_history.set_index(
            "Job"
        )["Threads Allocated"]
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Cloud-Based Intelligent Workload Scheduler | "
    "OpenMP High-Performance Computing Prototype"
)