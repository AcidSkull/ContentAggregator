from celery import Celery
from config import *


def make_celery(app):
    app.config['timezone'] = TIMEZONE
    app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
    app.config['result_backend'] = CELERY_RESULT_BACKEND
    app.config['beat_schelude'] = {
        'peridoic_task-every-minute' : {
            'task' : 'check_for_news',
            'schedule' : PERIOD_BETWEEN_TASK
        }
    }

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
