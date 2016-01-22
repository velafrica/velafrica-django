# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import simple_history.models
import datetime
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
                ('image', django_resized.forms.ResizedImageField(help_text=b'Product picture.', null=True, upload_to=b'stock/categories/', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', simple_history.models.CurrentUserField(related_name='_category_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
            },
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('sku', models.CharField(max_length=255, verbose_name=b'SKU', db_index=True)),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('category', models.IntegerField(db_index=True, null=True, verbose_name=b'Category', blank=True)),
                ('image', django_resized.forms.ResizedImageField(help_text=b'Product picture.', null=True, upload_to=b'stock/products/', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField(default=datetime.datetime.now)),
                ('history_type', models.CharField(max_length=1, choices=[(b'+', b'Created'), (b'~', b'Changed'), (b'-', b'Deleted')])),
                ('history_user', simple_history.models.CurrentUserField(related_name='_product_history', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date',),
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
