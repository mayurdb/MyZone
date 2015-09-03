# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20150625_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend_request',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('from_friend_req', models.ForeignKey(related_name='from_friend_req_set', to='myapp.User_profile')),
                ('to_friend_req', models.ForeignKey(related_name='to_friend_req_set', to='myapp.User_profile')),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('from_friend', models.ForeignKey(related_name='to_friend_set', to='myapp.User_profile')),
                ('to_friend', models.ForeignKey(related_name='friend_set', to='myapp.User_profile')),
            ],
        ),
        migrations.AlterField(
            model_name='child',
            name='image',
            field=models.ImageField(null=True, upload_to='', blank=True, default=None, storage=django.core.files.storage.FileSystemStorage(location='/myapp/photos')),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('to_friend', 'from_friend')]),
        ),
    ]
