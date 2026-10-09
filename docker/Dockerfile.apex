# Stage 1: Dependency Builder
FROM python:3.11-slim as builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime Environment
FROM python:3.11-slim
WORKDIR /app

# Install runtime security tooling (e.g., for eBPF and network trace support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    bpfcc-tools \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY src/ /app/src/
COPY config/ /app/config/
COPY AGENTS.md /app/

ENV PYTHONPATH=/app
ENTRYPOINT ["python", "-m", "src.cli.main"]
CMD ["stream", "--target", "workspace"]
