import sys

from app.core.celery_app import celery_app


def test_macos_worker_avoids_native_unsafe_prefork_pool():
    if sys.platform == "darwin":
        assert celery_app.conf.worker_pool == "solo"
        assert celery_app.conf.worker_concurrency == 1
