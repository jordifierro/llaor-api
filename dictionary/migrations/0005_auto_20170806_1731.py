# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-06 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_definition_semantic_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='definition',
            options={'ordering': ('word', 'semantic_group')},
        ),
        migrations.RemoveField(
            model_name='definition',
            name='priority',
        ),
    ]