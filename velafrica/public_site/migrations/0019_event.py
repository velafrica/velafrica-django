# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-12 13:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0034_auto_20161101_1151'),
        ('organisation', '0001_squashed_0022_auto_20160809_2049'),
        ('public_site', '0018_references_sorting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Beschreibung')),
                ('organizer', models.CharField(max_length=255, verbose_name=b'Veranstalter')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pub_event_address', to='organisation.Address', verbose_name=b'Adresse')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pub_event_category', to='collection.EventCategory', verbose_name=b'Kategorie')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]