# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0004_auto_20150811_0207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='abrevation',
            new_name='abreviation',
        ),
    ]
