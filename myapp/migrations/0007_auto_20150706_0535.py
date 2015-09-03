# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20150701_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='image',
            field=models.ImageField(default=None, upload_to='/images/', blank=True, null=True),
        ),
    ]
