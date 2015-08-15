# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0013_auto_20150815_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolcoursevalue',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'state', default=2, to='restserver.City', chained_field=b'state'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolcoursevalue',
            name='country',
            field=models.ForeignKey(default=1, to='restserver.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolcoursevalue',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'country', default=1, to='restserver.State', chained_field=b'country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schoolcoursevalue',
            name='school',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'city', to='restserver.School', chained_field=b'city'),
        ),
    ]
