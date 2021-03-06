# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-19 12:45
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import velafrica.core.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articlenr_start', models.CharField(blank=True, help_text=b'', max_length=8, null=True, unique=True, verbose_name=b'Kategorienummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(blank=True, null=True, verbose_name=b'Beschreibung')),
                ('image', django_resized.forms.ResizedImageField(blank=True, help_text=b'Product picture.', null=True, storage=velafrica.core.storage.MyStorage(), upload_to=b'stock/categories/')),
                ('color', models.CharField(blank=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', max_length=7, null=True, validators=[django.core.validators.RegexValidator(code=b'invalid_hexcode', message=b'Must be a hexcode (e.g. #000 or #000000)', regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])),
            ],
            options={
                'ordering': ['articlenr_start', 'name'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCategory',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('articlenr_start', models.CharField(blank=True, db_index=True, help_text=b'', max_length=8, null=True, verbose_name=b'Kategorienummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Kategoriebezeichnung')),
                ('description', models.TextField(blank=True, null=True, verbose_name=b'Beschreibung')),
                ('image', models.TextField(blank=True, help_text=b'Product picture.', max_length=100, null=True)),
                ('color', models.CharField(blank=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', max_length=7, null=True, validators=[django.core.validators.RegexValidator(code=b'invalid_hexcode', message=b'Must be a hexcode (e.g. #000 or #000000)', regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('articlenr', models.CharField(db_index=True, help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', max_length=7, verbose_name=b'Artikelnummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('name_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Produktbezeichnung FR')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Produktbezeichnung EN')),
                ('hscode', models.CharField(max_length=7, verbose_name=b'Harmonized System Code')),
                ('description', models.TextField(blank=True, help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung')),
                ('image', models.TextField(blank=True, max_length=100, null=True, verbose_name=b'Produktbild')),
                ('sales_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name=b'Verkaufspreis')),
                ('packaging_unit', models.IntegerField(blank=True, null=True, verbose_name=b'Verpackungseinheit (VE)')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Category')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical product',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStock',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, help_text=b'Anzahl der Produkte an Lager', verbose_name=b'St\xc3\xbcckzahl')),
                ('last_modified', models.DateTimeField(blank=True, editable=False, help_text=b'Tag und Zeit wann das Objekt zuletzt ge\xc3\xa4ndert wurde.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockList',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('last_change', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Stock Liste',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockListPosition',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Stock List Position',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockTransfer',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name=b'Ausf\xc3\xbchrdatum')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Bemerkungen')),
                ('booked', models.BooleanField(default=False, help_text=b'Gibt an ob der Stock bereits angepasst wurde.')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Stock Transfer',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWarehouse',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Der Name / Bezeichnung des Lagers', max_length=255, verbose_name=b'Name')),
                ('description', models.CharField(blank=True, help_text=b'Beschreibung / Bemerkungen zum Lager', max_length=255, null=True, verbose_name=b'Beschreibung')),
                ('image', models.TextField(blank=True, max_length=100, null=True, verbose_name=b'Bild des Lagers')),
                ('stock_management', models.BooleanField(default=False, help_text=b'Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.', verbose_name=b'Automatisches Stock-Management')),
                ('notify_on_incoming_transport', models.TextField(blank=True, help_text=b'Eine Emailadressen pro Zeile. Hier eingetragene Emailadressen werden jedesmal benachrichtigt, sobald eine neue Fahrt  mit Ersatzteilen zu diesem Lager erfasst wird.', null=True, verbose_name=b'\xc3\x9cber angeliferte Ersatzteile informieren')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Erstellt am'), ('~', 'Ge\xe4ndert'), ('-', 'Deleted')], max_length=1)),
                ('address', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organisation.Address')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organisation.Organisation')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical warehouse',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articlenr', models.CharField(help_text=b'Die Velafrica Artikelnummer (in der Form 123.123)', max_length=7, unique=True, verbose_name=b'Artikelnummer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Produktbezeichnung')),
                ('name_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Produktbezeichnung FR')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Produktbezeichnung EN')),
                ('hscode', models.CharField(max_length=7, verbose_name=b'Harmonized System Code')),
                ('description', models.TextField(blank=True, help_text=b'Hinweise zur Qualit\xc3\xa4t bzw Hinweise und Erg\xc3\xa4nzung', null=True, verbose_name=b'Beschreibung')),
                ('image', django_resized.forms.ResizedImageField(blank=True, null=True, storage=velafrica.core.storage.MyStorage(), upload_to=b'stock/products/', verbose_name=b'Produktbild')),
                ('sales_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name=b'Verkaufspreis')),
                ('packaging_unit', models.IntegerField(blank=True, null=True, verbose_name=b'Verpackungseinheit (VE)')),
                ('category', models.ForeignKey(help_text=b'Die Hauptkategorie des Produktes.', on_delete=django.db.models.deletion.CASCADE, to='stock.Category', verbose_name=b'Kategorie')),
            ],
            options={
                'ordering': ['articlenr'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, help_text=b'Anzahl der Produkte an Lager', verbose_name=b'St\xc3\xbcckzahl')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text=b'Tag und Zeit wann das Objekt zuletzt ge\xc3\xa4ndert wurde.')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Product', verbose_name=b'Produkt')),
            ],
            options={
                'ordering': ['warehouse', 'product'],
                'permissions': (('is_admin', 'Stock Admin - Can edit all stocks from every warehouse.'),),
            },
        ),
        migrations.CreateModel(
            name='StockChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('stock_change_type', models.CharField(choices=[(b'out', b'out'), (b'in', b'in')], max_length=255)),
                ('booked', models.BooleanField(default=False, help_text=b'Indicates if stock adjustments have been made.')),
            ],
            options={
                'verbose_name': 'Stock Change',
                'verbose_name_plural': 'Stock Changes',
            },
        ),
        migrations.CreateModel(
            name='StockChangeListPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
                ('stockchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockChange')),
            ],
            options={
                'verbose_name': 'Stock Change List Position',
                'verbose_name_plural': 'Stock Change List Positions',
            },
        ),
        migrations.CreateModel(
            name='StockList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Stock Liste',
                'verbose_name_plural': 'Stock Listen',
            },
        ),
        migrations.CreateModel(
            name='StockListPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
                ('stocklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockList', verbose_name=b'StockList')),
            ],
            options={
                'verbose_name': 'Stock List Position',
                'verbose_name_plural': 'Stock List Positionen',
            },
        ),
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name=b'Ausf\xc3\xbchrdatum')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Bemerkungen')),
                ('booked', models.BooleanField(default=False, help_text=b'Gibt an ob der Stock bereits angepasst wurde.')),
                ('stocklist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.StockList', verbose_name=b'Stock List')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Stock Transfer',
                'verbose_name_plural': 'Stock Transfers',
            },
        ),
        migrations.CreateModel(
            name='StockTransferListPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Product')),
                ('stocktransfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer')),
            ],
            options={
                'verbose_name': 'Stock Transfer List Position',
                'verbose_name_plural': 'Stock Transfers List Positionen',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Der Name / Bezeichnung des Lagers', max_length=255, verbose_name=b'Name')),
                ('description', models.CharField(blank=True, help_text=b'Beschreibung / Bemerkungen zum Lager', max_length=255, null=True, verbose_name=b'Beschreibung')),
                ('image', django_resized.forms.ResizedImageField(blank=True, null=True, storage=velafrica.core.storage.MyStorage(), upload_to=b'stock/warehouses/', verbose_name=b'Bild des Lagers')),
                ('stock_management', models.BooleanField(default=False, help_text=b'Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.', verbose_name=b'Automatisches Stock-Management')),
                ('notify_on_incoming_transport', models.TextField(blank=True, help_text=b'Eine Emailadressen pro Zeile. Hier eingetragene Emailadressen werden jedesmal benachrichtigt, sobald eine neue Fahrt  mit Ersatzteilen zu diesem Lager erfasst wird.', null=True, verbose_name=b'\xc3\x9cber angeliferte Ersatzteile informieren')),
                ('address', models.ForeignKey(blank=True, help_text=b'Nur angeben wenn die Lageradresse von Organisationsadresse abweicht.', null=True, on_delete=django.db.models.deletion.CASCADE, to='organisation.Address', verbose_name=b'Andere Adresse als Organisation')),
                ('organisation', models.ForeignKey(help_text=b'Die Organisation zu welcher das Lager geh\xc3\xb6rt. (Nur VPN Schweiz Partner)', on_delete=django.db.models.deletion.CASCADE, to='organisation.Organisation', verbose_name=b'Organisation')),
            ],
            options={
                'ordering': ['organisation', 'name'],
            },
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_from', to='stock.Warehouse', verbose_name=b'Herkunfts-Lager'),
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='warehouse_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_to', to='stock.Warehouse', verbose_name=b'Ziel-Lager'),
        ),
        migrations.AddField(
            model_name='stockchange',
            name='stocklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockList'),
        ),
        migrations.AddField(
            model_name='stockchange',
            name='stocktransfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer'),
        ),
        migrations.AddField(
            model_name='stockchange',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(help_text=b'Das Lager wo sich der Stock befindet', on_delete=django.db.models.deletion.CASCADE, to='stock.Warehouse', verbose_name=b'Lager'),
        ),
        migrations.AddField(
            model_name='historicalstocktransfer',
            name='stocklist',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.StockList'),
        ),
        migrations.AddField(
            model_name='historicalstocktransfer',
            name='warehouse_from',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='historicalstocktransfer',
            name='warehouse_to',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='historicalstocklistposition',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Product'),
        ),
        migrations.AddField(
            model_name='historicalstocklistposition',
            name='stocklist',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.StockList'),
        ),
        migrations.AddField(
            model_name='historicalstock',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Product'),
        ),
        migrations.AddField(
            model_name='historicalstock',
            name='warehouse',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.Warehouse'),
        ),
        migrations.AlterUniqueTogether(
            name='stocktransferlistpos',
            unique_together=set([('stocktransfer', 'product')]),
        ),
        migrations.AlterUniqueTogether(
            name='stocklistposition',
            unique_together=set([('stocklist', 'product')]),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('product', 'warehouse')]),
        ),
    ]
