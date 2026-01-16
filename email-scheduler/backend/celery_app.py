from celery import Celery
from config import settings

celery_app = Celery(
    'email_scheduler',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['tasks.email_tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,
    broker_connection_retry_on_startup=True,
)
