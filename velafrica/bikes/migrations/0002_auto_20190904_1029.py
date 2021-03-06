# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-04 08:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import velafrica.bikes.models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike',
            name='visum',
        ),
        migrations.AddField(
            model_name='bike',
            name='visa',
            field=models.CharField(blank=True, max_length=255, verbose_name='Visa'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='brake',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Brake'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='colour',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Colour'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='drivetrain',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Drivetrain'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='extraordinary',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Extraordinary'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='gearing',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Group of components'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=velafrica.bikes.models.bike_images, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='number',
            field=models.IntegerField(default=velafrica.bikes.models.next_a_plus_number, unique=True, verbose_name='No.'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='size',
            field=models.CharField(blank=True, choices=[('', '-'), ('S', 'S'), ('M', 'M'), ('L', 'L')], default='', max_length=255, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='suspension',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Suspension'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='type',
            field=models.CharField(choices=[('', '-'), ('MTB', 'MTB'), ('Touring Woman', 'Touring Woman'), ('Touring Man', 'Touring Man'), ('Kids', 'Kids'), ('Classic', 'Classic'), ('Racing', 'Racing')], max_length=255, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='type_of_brake',
            field=models.CharField(blank=True, choices=[('', '-'), ('Hydr. Disc', 'Hydraulic Disc'), ('Rim Brake', 'Rim brake')], default='', max_length=255, verbose_name='Type of Brake'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock.Warehouse', verbose_name='Warehouse'),
        ),
    ]
