# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0003_auto_20150811_0154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='costofliving',
            options={'verbose_name_plural': 'Costs of Living'},
        ),
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(default=1, to='restserver.Country'),
            preserve_default=False,
        ),
    ]
