# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0011_auto_20150812_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='abreviation',
            new_name='abbreviation',
        ),
    ]
