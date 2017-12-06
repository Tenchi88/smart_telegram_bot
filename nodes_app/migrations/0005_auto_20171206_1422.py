# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodes_app', '0004_auto_20171206_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='parent_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_nodes', related_query_name='sub_node', to='nodes_app.Node'),
        ),
    ]
