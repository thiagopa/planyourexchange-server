# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0007_auto_20150811_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'country', chained_field=b'country', auto_choose=True, to='restserver.State'),
        ),
    ]
