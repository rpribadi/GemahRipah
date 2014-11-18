# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('discount', models.DecimalField(default=0, max_digits=10, decimal_places=1)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('supplier', models.ForeignKey(to='products.Merchant')),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(max_digits=10, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(to='products.Product')),
                ('purchase', models.ForeignKey(to='purchase.Purchase')),
            ],
            options={
                'ordering': ('product__name',),
            },
            bases=(models.Model,),
        ),
    ]
