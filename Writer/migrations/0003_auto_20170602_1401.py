# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Writer', '0002_auto_20170114_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除（取消关注）')),
            ],
        ),
        migrations.AddField(
            model_name='writer',
            name='total_follow',
            field=models.IntegerField(default=0, verbose_name='我的关注'),
        ),
        migrations.AddField(
            model_name='writer',
            name='total_followed',
            field=models.IntegerField(default=0, verbose_name='我的粉丝'),
        ),
        migrations.AddField(
            model_name='follow',
            name='followee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee', to='Writer.Writer', verbose_name='关注者'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='Writer.Writer', verbose_name='追随者'),
        ),
    ]