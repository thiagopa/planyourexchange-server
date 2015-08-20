# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0015_auto_20150820_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airtrip',
            name='airport_layover',
            field=models.DurationField(null=True, blank=True),
        ),
    ]
