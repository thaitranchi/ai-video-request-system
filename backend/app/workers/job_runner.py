import os
from celery import Celery
from app.services.video_pipeline import video_pipeline

# Configuration for Celery to use RabbitMQ as broker and Redis as backend
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq-service:5672//")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "video_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

@celery_app.task(name="process_video_request")
def process_request_task(request_id: str, query: str):
    """
    Celery worker task that wraps the video pipeline.
    """
    return video_pipeline.process_request(request_id, query)