# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-13 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Photo',
            new_name='Fileup',
        ),
    ]