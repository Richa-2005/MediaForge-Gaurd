from app.core.config import settings
from celery import Celery
from kombu import Queue
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
    task_ignore_result=True,
    result_persistent=False,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
   
    worker_pool="solo" if sys.platform == "darwin" else "prefork",
    worker_concurrency=1 if sys.platform == "darwin" else None,
    task_default_queue="celery",
    task_queues=(
        Queue("celery"),
        Queue("image_queue"),
        Queue("text_queue"),
        Queue("video_queue"),
        Queue("audio_queue"),
    ),
)

if settings.CELERY_BROKER_URL.startswith("rediss://"):
    celery_app.conf.broker_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }

if settings.CELERY_RESULT_BACKEND.startswith("rediss://"):
    celery_app.conf.redis_backend_use_ssl = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }
