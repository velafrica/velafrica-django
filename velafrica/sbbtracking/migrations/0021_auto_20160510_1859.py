# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sbbtracking', '0020_auto_20160510_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalVeloType',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Bezeichnung')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical velo type',
            },
        ),
        migrations.CreateModel(
            name='VeloType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Bezeichnung')),
            ],
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='velo_type',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.VeloType', null=True),
        ),
        migrations.AddField(
            model_name='tracking',
            name='velo_type',
            field=models.ForeignKey(blank=True, to='sbbtracking.VeloType', null=True),
        ),
    ]
