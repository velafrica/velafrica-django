# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('velafrica_sud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forwarder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name des Forwarders')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalForwarder',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name des Forwarders')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical forwarder',
            },
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['-name'], 'verbose_name_plural': 'Countries'},
        ),
        migrations.RemoveField(
            model_name='container',
            name='logistics'
        ),
        migrations.AddField(
            model_name='container',
            name='logistics',
            field=models.ForeignKey(to='velafrica_sud.Forwarder', blank=True, help_text=b'Logistikunternehmen', null=True, verbose_name=b'Forwarder'),
        ),
        migrations.AlterField(
            model_name='container',
            name='pickup_date',
            field=models.DateField(verbose_name=b'Ladedatum'),
        ),
        migrations.RemoveField(
            model_name='historicalcontainer',
            name='logistics'
        ),
        migrations.AddField(
            model_name='historicalcontainer',
            name='logistics',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='velafrica_sud.Forwarder', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcontainer',
            name='pickup_date',
            field=models.DateField(verbose_name=b'Ladedatum'),
        ),
    ]
