# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20150625_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='grade',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='child',
            name='image',
            field=models.ImageField(upload_to='', blank=True, null=True, default=None, storage=django.core.files.storage.FileSystemStorage(location='/myapp/photos/')),
        ),
    ]
