from celery.schedules import crontab

broker_connection_retry_on_startup = True
enable_utc = True

imports = ("bot_engine.tasks.live", "bot_engine.tasks.scheduled")

task_routes = {
    "bot_engine.tasks.live": {"queue": "live"},
    "bot_engine.tasks.scheduled": {"queue": "scheduled"},
}

beat_schedule = {
    "check-prices-every-day": {
        "task": "check_price",
        "schedule": crontab(hour="12", minute="0"),
    },
}
