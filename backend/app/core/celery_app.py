from app.core.config import settings
from celery import Celery
import ssl
import sys

celery_app = Celery(
    "mediaforge-guard",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.upload_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # Native CV/ML libraries can abort a forked process on macOS.
    # The solo pool avoids unsafe post-fork native initialization.
    worker_pool="solo" if sys.platform == "darwin" else "prefork",
    worker_concurrency=1 if sys.platform == "darwin" else None,
)

if settings.CELERY_BROKER_URL.startswith("rediss://"):
    celery_app.conf.broker_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }

if settings.CELERY_RESULT_BACKEND.startswith("rediss://"):
    celery_app.conf.redis_backend_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }
