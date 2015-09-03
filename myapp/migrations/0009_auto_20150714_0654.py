# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20150706_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='image',
            field=models.ImageField(default=None, null=True, blank=True, upload_to='images/'),
        ),
    ]
