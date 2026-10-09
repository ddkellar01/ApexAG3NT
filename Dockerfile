# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies for C-extensions and code verification
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install common testing and AST parsing tools
RUN pip install --no-cache-dir \
    pytest \
    mypy \
    black \
    flake8 \
    astor \
    pydantic

# Default command keeps the container alive for REPL bindings
CMD ["tail", "-f", "/dev/null"]
