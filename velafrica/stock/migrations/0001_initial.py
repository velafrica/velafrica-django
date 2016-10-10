# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_auto_20160202_1454'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('articlenr_start', models.CharField(null=True, max_length=8, blank=True, help_text=b'', unique=True, verbose_name=b'Kategorienummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', django_resized.forms.ResizedImageField(help_text=b'Product picture.', null=True, upload_to=b'stock/categories/', blank=True)),
                ('color', models.CharField(blank=True, max_length=7, null=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Must be a hexcode (e.g. #000 or #000000)', code=b'invalid_hexcode')])),
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
                ('articlenr_start', models.CharField(max_length=8, blank=True, help_text=b'', null=True, verbose_name=b'Kategorienummer', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', models.TextField(help_text=b'Product picture.', max_length=100, null=True, blank=True)),
                ('color', models.CharField(blank=True, max_length=7, null=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Must be a hexcode (e.g. #000 or #000000)', code=b'invalid_hexcode')])),
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
                ('articlenr', models.CharField(help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', max_length=7, verbose_name=b'Artikelnummer', db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('hscode', models.CharField(max_length=7, verbose_name=b'Harmonized System Code')),
                ('description', models.TextField(help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', models.TextField(max_length=100, null=True, verbose_name=b'Produktbild', blank=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
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
                ('articlenr', models.CharField(help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', unique=True, max_length=7, verbose_name=b'Artikelnummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('hscode', models.CharField(max_length=7, verbose_name=b'Harmonized System Code')),
                ('description', models.TextField(help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', django_resized.forms.ResizedImageField(upload_to=b'stock/products/', null=True, verbose_name=b'Produktbild', blank=True)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('category', models.ForeignKey(verbose_name=b'Kategorie', to='stock.Category', help_text=b'Die Hauptkategorie des Produktes.')),
            ],
            options={
                'ordering': ['articlenr'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=0, help_text=b'Anzahl der Produkte an Lager', verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(verbose_name=b'Produkt', to='stock.Product')),
            ],
            options={
                'ordering': ['warehouse', 'product'],
            },
        ),
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Ausf\xc3\xbchrdatum')),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'Bemerkungen', blank=True)),
                ('booked', models.BooleanField(default=False, help_text=b'Gibt an ob der Stock bereits angepasst wurde.')),
                ('executor', models.ForeignKey(verbose_name=b'Ausf\xc3\xbchrende Person', to='organisation.Person', help_text=b'Die Person welche die Verschiebung vorgenommen hat.')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='StockTransferPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(to='stock.Product')),
                ('stocktransfer', models.ForeignKey(verbose_name=b'Der zugeh\xc3\xb6rige StockTransfer', to='stock.StockTransfer')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Der Name / Bezeichnung des Lagers', max_length=255, verbose_name=b'Name')),
                ('description', models.CharField(help_text=b'Beschreibung / Bemerkungen zum Lager', max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', django_resized.forms.ResizedImageField(upload_to=b'stock/warehouses/', null=True, verbose_name=b'Bild des Lagers', blank=True)),
                ('stock_management', models.BooleanField(default=False, help_text=b'Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.', verbose_name=b'Automatisches Stock-Management')),
                ('organisation', models.ForeignKey(verbose_name=b'Organisation', to='organisation.Organisation', help_text=b'Die Organisation zu welcher das Lager geh\xc3\xb6rt.')),
            ],
            options={
                'ordering': ['organisation', 'name'],
            },
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_from',
            field=models.ForeignKey(related_name='warehouse_from', verbose_name=b'Herkunfts-Lager', to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_to',
            field=models.ForeignKey(related_name='warehouse_to', verbose_name=b'Ziel-Lager', to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(verbose_name=b'Lager', to='stock.Warehouse', help_text=b'Das Lager wo sich der Stock befindet'),
        ),
        migrations.AlterUniqueTogether(
            name='stocktransferposition',
            unique_together=set([('stocktransfer', 'product')]),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('product', 'warehouse')]),
        ),
    ]
