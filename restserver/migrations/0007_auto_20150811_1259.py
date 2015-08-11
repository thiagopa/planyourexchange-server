# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0006_auto_20150811_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='address',
        ),
        migrations.AddField(
            model_name='school',
            name='address_line',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='suburb',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='zip_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
