# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0008_auto_20150811_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='country',
            field=models.ForeignKey(default=1, to='restserver.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'country', default=1, to='restserver.State', chained_field=b'country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'state', to='restserver.City', chained_field=b'state'),
        ),
    ]
