# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 09:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20171021_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='is_deleted',
        ),
    ]