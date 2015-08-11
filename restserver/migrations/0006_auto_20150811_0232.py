# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0005_auto_20150811_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.OneToOneField(to='restserver.Address'),
        ),
    ]
