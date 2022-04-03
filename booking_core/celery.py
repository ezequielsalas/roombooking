import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from booking_core import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_core.settings')

app = Celery('roombooking')
app.conf.ONCE = settings.CELERY_ONCE

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')