# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-22 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0009_auto_20181122_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeereference',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
