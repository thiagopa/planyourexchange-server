# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0018_auto_20150820_0601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airtrip',
            options={'ordering': ['trip_sequence']},
        ),
        migrations.AddField(
            model_name='airtrip',
            name='trip_sequence',
            field=models.IntegerField(default=1),
        ),
    ]
