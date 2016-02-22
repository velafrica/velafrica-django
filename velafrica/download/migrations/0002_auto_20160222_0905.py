# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Dateiname')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('category_parent', models.ForeignKey(help_text=b'\xc3\x9cbergeordnete Kategorie', to='download.Category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalCategory',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Dateiname')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('category_parent', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='download.Category', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical category',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='category',
            field=models.ForeignKey(blank=True, null=True, to='download.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalfile',
            name='category',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='download.Category', null=True),
        ),
    ]
