import time
import logging
from prometheus_client import start_http_server, Gauge
from app.workers.job_runner import celery_app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a Prometheus Gauge metric
CELERY_QUEUE_LENGTH = Gauge(
    'celery_queue_length',
    'Number of tasks waiting in the Celery queue',
    ['queue_name']
)

def monitor_queue(queue_name="celery"):
    logger.info(f"Starting queue monitor for: {queue_name}")
    while True:
        try:
            # Acquire a connection to the broker (RabbitMQ)
            with celery_app.connection_or_acquire() as conn:
                # passive=True ensures we only inspect the queue without creating/modifying it
                res = conn.default_channel.queue_declare(queue=queue_name, passive=True)
                CELERY_QUEUE_LENGTH.labels(queue_name=queue_name).set(res.message_count)
        except Exception as e:
            logger.error(f"Error fetching queue size: {e}")
        
        time.sleep(15)  # Align with your Prometheus scrape interval

if __name__ == "__main__":
    # Expose the metrics on port 8001
    start_http_server(8001)
    monitor_queue()