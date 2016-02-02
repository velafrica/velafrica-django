# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_auto_20160129_1010'),
        ('stock', '0002_stock_stockinout_stockmovement_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Ausf\xc3\xbchrdatum')),
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
            ],
        ),
        migrations.DeleteModel(
            name='StockInOut',
        ),
        migrations.DeleteModel(
            name='StockMovement',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['articlenr']},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['warehouse', 'product']},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ['organisation', 'name']},
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='sku',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.AddField(
            model_name='category',
            name='articlenr_start',
            field=models.CharField(null=True, max_length=7, blank=True, help_text=b'', unique=True, verbose_name=b'Erste Nummer des Artikelnummerbereiches'),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='articlenr_start',
            field=models.CharField(max_length=7, blank=True, help_text=b'', null=True, verbose_name=b'Erste Nummer des Artikelnummerbereiches', db_index=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='articlenr',
            field=models.CharField(default=b'000.000', help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', max_length=7, verbose_name=b'Artikelnummer', db_index=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='hscode',
            field=models.CharField(default=b'0000.00', max_length=7, verbose_name=b'Harmonized System Code'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='price',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='articlenr',
            field=models.CharField(default=b'000.000', help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', unique=True, max_length=7, verbose_name=b'Artikelnummer'),
        ),
        migrations.AddField(
            model_name='product',
            name='hscode',
            field=models.CharField(default=b'0000.00', max_length=7, verbose_name=b'Harmonized System Code'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='amount',
            field=models.IntegerField(default=0, help_text=b'Anzahl der Produkte an Lager', verbose_name=b'St\xc3\xbcckzahl'),
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(default=1, verbose_name=b'Produkt', to='stock.Product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(default=1, verbose_name=b'Lager', to='stock.Warehouse', help_text=b'Das Lager wo sich der Stock befindet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='description',
            field=models.CharField(help_text=b'Beschreibung / Bemerkungen zum Lager', max_length=255, null=True, verbose_name=b'Beschreibung', blank=True),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='image',
            field=django_resized.forms.ResizedImageField(upload_to=b'stock/warehouses/', null=True, verbose_name=b'Bild des Lagers', blank=True),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='name',
            field=models.CharField(default='name', help_text=b'Der Name / Bezeichnung des Lagers', max_length=255, verbose_name=b'Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='organisation',
            field=models.ForeignKey(default=1, verbose_name=b'Lager', to='organisation.Organisation', help_text=b'Die Organisation zu welcher das Lager geh\xc3\xb6rt.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='description',
            field=models.TextField(help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalproduct',
            name='image',
            field=models.TextField(max_length=100, null=True, verbose_name=b'Produktbild', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(verbose_name=b'Kategorie', to='stock.Category', help_text=b'Die Hauptkategorie des Produktes.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(upload_to=b'stock/products/', null=True, verbose_name=b'Produktbild', blank=True),
        ),
        migrations.AddField(
            model_name='stocktransferposition',
            name='product',
            field=models.ForeignKey(to='stock.Product'),
        ),
        migrations.AddField(
            model_name='stocktransferposition',
            name='stocktransfer',
            field=models.ForeignKey(verbose_name=b'Der zugeh\xc3\xb6rige StockTransfer', to='stock.StockTransfer'),
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_from',
            field=models.ForeignKey(related_name='warehouse_from', to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_to',
            field=models.ForeignKey(related_name='warehouse_to', to='stock.Warehouse'),
        ),
    ]
