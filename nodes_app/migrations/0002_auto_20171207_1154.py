# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 11:54
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nodes_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='parent_node',
        ),
        migrations.AddField(
            model_name='node',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='nodes_app.Node'),
        ),
    ]
