# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 05:23
from __future__ import unicode_literals

from django.db import migrations, models
import fileapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('fileapp', '0006_auto_20181015_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileup',
            name='file',
            field=models.FileField(upload_to=fileapp.models.document_directory_path),
        ),
    ]