# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20150630_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend_request',
            name='is_accepted',
        ),
    ]
