# Use Python 3.13 slim as base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure Python output is sent straight to terminal (useful for logs)
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install mcp-proxy using uv
RUN uv tool install mcp-proxy

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application code
COPY main.py ./

# Expose port (default 8080, can be overridden by PORT env var)
EXPOSE 8080

# Set PORT environment variable (can be overridden at runtime)
ENV PORT=8080

# Use mcp-proxy to wrap stdio MCP server with SSE
# --pass-environment passes all environment variables to the child process
# Using shell form to allow PORT variable expansion
ENTRYPOINT mcp-proxy --port=${PORT:-8080} --host 0.0.0.0 --allow-origin "*" --pass-environment -- uv run main.py
