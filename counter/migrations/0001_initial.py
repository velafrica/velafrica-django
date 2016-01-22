# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import simple_history.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Datum und Uhrzeit')),
                ('amount', models.IntegerField(verbose_name=b'Anzahl Velos')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Datum und Uhrzeit')),
                ('amount', models.IntegerField(verbose_name=b'Anzahl Velos')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', simple_history.models.CurrentUserField(related_name='_entry_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
        ),
    ]
