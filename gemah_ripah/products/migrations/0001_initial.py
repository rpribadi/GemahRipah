# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', products.models.CharUpperCaseField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', products.models.CharUpperCaseField(unique=True, max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=1)),
                ('stock', models.IntegerField(default=0)),
                ('brand', models.ForeignKey(to='products.Brand')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
