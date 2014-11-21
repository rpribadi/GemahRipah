# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20141120_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
