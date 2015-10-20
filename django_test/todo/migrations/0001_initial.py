# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=20)),
                ('mobile', models.IntegerField(max_length=10, serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
    ]
