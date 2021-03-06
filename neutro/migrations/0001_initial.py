# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-04 22:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientID', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PatientLabs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('labtype', models.IntegerField(default=0)),
                ('labvalue', models.IntegerField(default=0)),
                ('patientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutro.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='PatientLabs2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('ancvalue', models.IntegerField(default=0)),
                ('serumvalue', models.IntegerField(default=0)),
                ('patientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutro.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='PatientVitals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('systolic', models.IntegerField(default=0)),
                ('diastolic', models.IntegerField(default=0)),
                ('heartrate', models.IntegerField(default=0)),
                ('temperature', models.FloatField(default=0)),
                ('patientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutro.Patient')),
            ],
        ),
    ]
