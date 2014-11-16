# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller', products.models.CharUpperCaseField(max_length=100)),
                ('product', products.models.CharUpperCaseField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=1)),
                ('promotion_price', models.DecimalField(null=True, max_digits=10, decimal_places=1)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', products.models.CharUpperCaseField(max_length=100)),
                ('name', products.models.CharUpperCaseField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=1)),
                ('stock', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('brand', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('brand', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='comparison',
            unique_together=set([('product', 'seller')]),
        ),
    ]
