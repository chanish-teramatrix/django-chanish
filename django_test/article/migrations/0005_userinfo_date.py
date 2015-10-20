# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_userinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 12, 7, 27, 25, 595069)),
        ),
    ]
