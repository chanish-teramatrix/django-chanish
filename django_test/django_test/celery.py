from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTING_MODULE','djnago_test.settings')

app = Celery('django_test')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))