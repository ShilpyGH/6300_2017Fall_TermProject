# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-04 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neutro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientlabs',
            name='labtype',
            field=models.CharField(default=0, max_length=250),
        ),
        migrations.AlterField(
            model_name='patientlabs',
            name='labvalue',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patientlabs2',
            name='ancvalue',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patientlabs2',
            name='serumvalue',
            field=models.FloatField(default=0),
        ),
    ]
