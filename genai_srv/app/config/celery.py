from celery import Celery

celery_app = Celery(
    "tasks",
    # TODO add env variable
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
)

celery_app.autodiscover_tasks(
    ["app.tasks.qdrant.upload_tasks.upload_to_qdrant"], force=True
)
