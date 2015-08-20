# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0017_auto_20150820_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airtrip',
            name='airport_layover',
            field=models.DurationField(default=datetime.timedelta(0), blank=True),
        ),
    ]
