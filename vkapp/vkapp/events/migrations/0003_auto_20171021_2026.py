# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_afisha_event_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.CharField(max_length=30, null=True),
        ),
    ]