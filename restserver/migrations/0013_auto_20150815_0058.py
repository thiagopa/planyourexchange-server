# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restserver', '0012_auto_20150814_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costofliving',
            name='public_transport_monthly_currency',
        ),
        migrations.RemoveField(
            model_name='costofliving',
            name='rent_average_monthly_currency',
        ),
        migrations.RemoveField(
            model_name='costofliving',
            name='restaurant_average_per_meal_currency',
        ),
        migrations.RemoveField(
            model_name='costofliving',
            name='super_market_average_per_month_currency',
        ),
        migrations.RemoveField(
            model_name='costofliving',
            name='utilites_average_monthly_currency',
        ),
        migrations.RemoveField(
            model_name='country',
            name='visa_fee_currency',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='company_website',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='couple_price_per_month_currency',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='familly_price_per_month_currency',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='id',
        ),
        migrations.RemoveField(
            model_name='healthinsurance',
            name='single_price_per_month_currency',
        ),
        migrations.RemoveField(
            model_name='school',
            name='books_fee_currency',
        ),
        migrations.RemoveField(
            model_name='school',
            name='enrolment_fee_currency',
        ),
        migrations.RemoveField(
            model_name='schoolcoursevalue',
            name='week_price_currency',
        ),
        migrations.AddField(
            model_name='healthinsurance',
            name='abstractmodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='restserver.AbstractModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='healthinsurance',
            name='website',
            field=models.URLField(default='http://www.bupa.com.au'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='public_transport_monthly',
            field=models.DecimalField(verbose_name=b'Monthly Public Transport ticket', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='rent_average_monthly',
            field=models.DecimalField(verbose_name=b'Average Rent per Month', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='restaurant_average_per_meal',
            field=models.DecimalField(verbose_name=b'Average meal in Restaurant', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='super_market_average_per_month',
            field=models.DecimalField(verbose_name=b'Average Supermarket per Month', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='costofliving',
            name='utilites_average_monthly',
            field=models.DecimalField(verbose_name=b'Average Utilites per Month', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='country',
            name='visa_fee',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='healthinsurance',
            name='couple_price_per_month',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='healthinsurance',
            name='familly_price_per_month',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='healthinsurance',
            name='single_price_per_month',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='school',
            name='books_fee',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='school',
            name='enrolment_fee',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='schoolcoursevalue',
            name='week_price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
