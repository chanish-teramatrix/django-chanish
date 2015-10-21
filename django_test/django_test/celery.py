from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
from celery.schedules import crontab
from celery import task


os.environ.setdefault('DJANGO_SETTING_MODULE','djnago_test.settings')

app = Celery('django_test')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('djanog.conf:settings')
app.autodiscover_task(lambda: settings.INSTALLED_APPS)