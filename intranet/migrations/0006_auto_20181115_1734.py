# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0005_remove_leaverequest_account_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'currencies'},
        ),
        migrations.AlterModelOptions(
            name='education',
            options={'verbose_name_plural': 'education'},
        ),
        migrations.AlterModelOptions(
            name='employeeleave',
            options={'verbose_name_plural': 'employee leave'},
        ),
        migrations.AlterModelOptions(
            name='providentfundbeneficiary',
            options={'verbose_name_plural': 'provident fund beneficiaries'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': 'user information'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
