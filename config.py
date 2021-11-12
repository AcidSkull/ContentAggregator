from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
PERIOD_BETWEEN_TASK = crontab(hour="*/6")
TIMEZONE = 'Europe/Warsaw'