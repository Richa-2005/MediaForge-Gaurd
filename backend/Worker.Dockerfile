FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        libmagic1 \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-worker.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-worker.txt

COPY backend ./backend
COPY ai_workers ./ai_workers

WORKDIR /app/backend

CMD ["celery", "-A", "app.core.celery_app.celery_app", "worker", "--loglevel=info", "--concurrency=1"]
