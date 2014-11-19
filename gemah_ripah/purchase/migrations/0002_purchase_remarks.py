# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='remarks',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
