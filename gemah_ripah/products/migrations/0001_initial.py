# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import gemah_ripah.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', gemah_ripah.models.CharUpperCaseField(unique=True, max_length=2)),
                ('name', gemah_ripah.models.CharUpperCaseField(unique=True, max_length=50)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('code',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', gemah_ripah.models.CharUpperCaseField(max_length=100)),
                ('name', gemah_ripah.models.CharUpperCaseField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_purchased', models.IntegerField(default=0)),
                ('total_sold', models.IntegerField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('brand', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductComparison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', gemah_ripah.models.CharUpperCaseField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('promotion_price', models.DecimalField(null=True, max_digits=10, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('product', models.ForeignKey(to='products.Product', null=True)),
                ('seller', models.ForeignKey(to='products.Merchant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productcomparison',
            unique_together=set([('seller', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('brand', 'name')]),
        ),
    ]
