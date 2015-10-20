# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_userinfo_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
