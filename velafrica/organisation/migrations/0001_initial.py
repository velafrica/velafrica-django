# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOrganisation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name der Organisation')),
                ('street', models.CharField(max_length=255, verbose_name=b'Strasse')),
                ('plz', models.IntegerField(verbose_name=b'PLZ')),
                ('city', models.CharField(max_length=255, verbose_name=b'Ort')),
                ('website', models.CharField(max_length=255, null=True, verbose_name=b'Website', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical organisation',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name der Organisation')),
                ('street', models.CharField(max_length=255, verbose_name=b'Strasse')),
                ('plz', models.IntegerField(verbose_name=b'PLZ')),
                ('city', models.CharField(max_length=255, verbose_name=b'Ort')),
                ('website', models.CharField(max_length=255, null=True, verbose_name=b'Website', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisation', models.ForeignKey(verbose_name=b'Arbeitgeber', to='organisation.Organisation')),
                ('user', models.ForeignKey(verbose_name=b'Django User Account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
