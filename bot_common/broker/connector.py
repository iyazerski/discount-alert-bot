from celery import Celery
from loguru import logger


class Broker:
    def __init__(self, dsn: str) -> None:
        self.app = Celery("discount-alert-bot", broker=dsn)

    def include_tasks(self, include: list[str]) -> None:
        self.app.conf.update(include=include)

    def send(self, task_data: dict, task_name: str, queue: str) -> None:
        task = self.app.send_task(task_name, kwargs=task_data, queue=queue)
        logger.info(f"Task {task_name}[{task.id}] sent to {queue}")
