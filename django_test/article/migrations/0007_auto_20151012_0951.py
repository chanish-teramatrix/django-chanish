# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20151012_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(max_length=10, choices=[(b'', b'Select'), (b'Male', b'male'), (b'Female', b'female')]),
        ),
    ]
