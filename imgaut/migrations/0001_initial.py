# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-29 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orimage', models.ImageField(null=True, upload_to='original')),
                ('elaimage', models.ImageField(null=True, upload_to='elaimage')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentAuthenticity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(null=True)),
                ('exifresult', models.IntegerField(null=True)),
                ('elaresult', models.IntegerField(null=True)),
                ('authenticity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='imgaut.Document')),
            ],
        ),
    ]
