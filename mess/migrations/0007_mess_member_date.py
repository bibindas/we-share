# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-12 05:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0006_auto_20170611_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='mess_member',
            name='date',
            field=models.CharField(default=datetime.datetime(2017, 6, 12, 5, 59, 36, 437164, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
