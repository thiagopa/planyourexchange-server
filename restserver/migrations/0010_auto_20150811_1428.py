# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0009_auto_20150811_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='costofliving',
            name='country',
            field=models.ForeignKey(default=1, to='restserver.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='costofliving',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'country', default=1, to='restserver.State', chained_field=b'country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'state', to='restserver.City', chained_field=b'state'),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='public_transport_monthly',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name=b'Monthly Public Transport ticket', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='rent_average_monthly',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name=b'Average Rent per Month', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='restaurant_average_per_meal',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name=b'Average meal in Restaurant', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='super_market_average_per_month',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name=b'Average Supermarket per Month', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='utilites_average_monthly',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), verbose_name=b'Average Utilites per Month', max_digits=10, decimal_places=2),
        ),
    ]
