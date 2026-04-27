# ---------- Stage 1: Builder ----------
FROM python:3.11.15-slim-trixie AS builder

WORKDIR /app

# Copy only required files (better caching)
COPY main.py version.py ./

# ---------- Stage 2: Runtime ----------
FROM python:3.11.15-slim-trixie

# Avoid Python cache + ensure logs go to stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy from builder (clean image)
COPY --from=builder /app /app

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root
USER appuser

# ENTRYPOINT + CMD separation
ENTRYPOINT ["python", "main.py"]
CMD ["--version"]