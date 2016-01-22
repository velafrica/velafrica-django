# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', django_resized.forms.ResizedImageField(help_text=b'Product picture.', null=True, upload_to=b'stock/categories/', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCategory',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', models.TextField(help_text=b'Product picture.', max_length=100, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical category',
            },
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('sku', models.CharField(max_length=255, verbose_name=b'SKU', db_index=True)),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', models.TextField(help_text=b'Product picture.', max_length=100, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('category', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Category', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical product',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('sku', models.CharField(unique=True, max_length=255, verbose_name=b'SKU')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', django_resized.forms.ResizedImageField(help_text=b'Product picture.', null=True, upload_to=b'stock/products/', blank=True)),
                ('category', models.ForeignKey(verbose_name=b'Category', to='stock.Category')),
            ],
            options={
                'ordering': ['sku'],
            },
        ),
    ]
