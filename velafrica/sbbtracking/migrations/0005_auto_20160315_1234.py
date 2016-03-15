# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sbbtracking', '0004_auto_20160315_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTrackingEventType',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('send_email', models.BooleanField(help_text=b'Aktivieren falls bei Erstellung eines Events dieser Art automatisch ein Email an den Spender versandt werden soll.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical tracking event type',
            },
        ),
        migrations.CreateModel(
            name='TrackingEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('send_email', models.BooleanField(help_text=b'Aktivieren falls bei Erstellung eines Events dieser Art automatisch ein Email an den Spender versandt werden soll.')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='historicaltrackingevent',
            name='event_type',
        ),
        migrations.RemoveField(
            model_name='trackingevent',
            name='event_type',
        ),
    ]
