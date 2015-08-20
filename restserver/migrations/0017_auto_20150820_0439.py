# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0016_auto_20150820_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='airport',
            field=models.CharField(default='SYD', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='is_flexible',
            field=models.BooleanField(default=False),
        ),
    ]
