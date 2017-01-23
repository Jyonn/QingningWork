# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Work', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='last_version_work',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Work.Work', verbose_name='上一版本的作品'),
        ),
        migrations.AddField(
            model_name='work',
            name='version_num',
            field=models.IntegerField(default=0, verbose_name='作品第几版'),
        ),
    ]