# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_friend_request_is_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='from_friend',
            field=models.ForeignKey(related_name='from_friend_set', to='myapp.User_profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to_friend',
            field=models.ForeignKey(related_name='to_friend_set', to='myapp.User_profile'),
        ),
        migrations.AlterUniqueTogether(
            name='friend_request',
            unique_together=set([('to_friend_req', 'from_friend_req')]),
        ),
    ]
