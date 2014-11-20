# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20141119_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='total_purchased',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='total_sold',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
    ]
