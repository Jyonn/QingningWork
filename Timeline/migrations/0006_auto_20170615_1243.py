# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Timeline', '0005_auto_20170607_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AbstractUser.AbstractUser', verbose_name='所属用户'),
        ),
    ]