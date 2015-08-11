# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0002_auto_20150811_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='restserver.State'),
        ),
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.ForeignKey(to='restserver.Address'),
        ),
    ]
