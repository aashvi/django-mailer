# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retention', '0013_auto_20170329_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]