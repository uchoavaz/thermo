from __future__ import absolute_import

import os
from celery.schedules import crontab
from celery import *
from django.conf import settings  # noqa
from decouple import config


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thermo_genomika.settings')

app = Celery('thermo_genomika', broker=config('CELERY_BROKER_URL'))

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
