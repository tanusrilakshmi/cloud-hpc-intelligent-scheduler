FROM python:3.12-slim

WORKDIR /app

# Install GCC, C development headers, and OpenMP runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Compile the OpenMP worker for Linux
RUN gcc -O2 -fopenmp workers/openmp_worker.c \
    -o workers/openmp_worker

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit configuration
EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501"]
     
