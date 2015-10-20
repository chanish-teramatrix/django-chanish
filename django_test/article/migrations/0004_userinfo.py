# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('dob', models.DateTimeField()),
                ('nick_name', models.CharField(max_length=8)),
                ('gender', models.CharField(max_length=10, choices=[(b'Male', b'male'), (b'Femail', b'female')])),
                ('password', models.CharField(max_length=8)),
            ],
        ),
    ]
