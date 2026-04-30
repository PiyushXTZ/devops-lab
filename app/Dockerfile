# ═══════════════════════════════════════════════
# STAGE 1 — builder
# Full Python image with build tools available.
# We install packages here — this stage is NEVER
# shipped to production, only its output is used.
# ═══════════════════════════════════════════════
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy only requirements first (layer cache optimisation)
COPY requirements.txt .

# Install packages into a local directory — not system-wide.
# --no-cache-dir removes the download cache.
# --prefix=/install puts packages in /build/install so we can
# copy ONLY that folder into the final stage.
RUN pip install \
    --no-cache-dir \
    --prefix=/build/install \
    -r requirements.txt


# ═══════════════════════════════════════════════
# STAGE 2 — final (production image)
# Starts completely fresh. No build tools, no pip,
# no cache. Just the app and the installed packages.
# This is the image that actually gets deployed.
# ═══════════════════════════════════════════════
FROM python:3.12-slim

WORKDIR /app

# Copy ONLY the installed packages from the builder stage
COPY --from=builder /build/install /usr/local

# Copy application code
COPY app.py .

# Runtime environment variables
ENV FLASK_ENV=production
ENV REDIS_HOST=redis
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run as non-root user for better security (optional but best practice)
RUN useradd --no-create-home appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
