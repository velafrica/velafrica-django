# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisation', '0004_auto_20160218_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('velos', models.IntegerField(default=0, verbose_name=b'Anzahl Velos')),
                ('velos_worth', models.IntegerField(default=0, verbose_name=b'Wert der Velos')),
                ('spare_parts', models.BooleanField(default=False, verbose_name=b'Ersatzteile transportiert?')),
                ('spare_parts_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('tools_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('various_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('pickup_date', models.DateField(verbose_name=b'Ladedatum beim Verarbeitungspartner')),
                ('shipment_date', models.DateField(null=True, verbose_name=b'Verschiffungsdatum ab Europa', blank=True)),
                ('arrival_port_date', models.DateField(null=True, verbose_name=b'Ankunft Hafen Partner', blank=True)),
                ('arrival_partner_date', models.DateField(null=True, verbose_name=b'Ankunft Partner', blank=True)),
                ('logistics', models.CharField(max_length=255, null=True, verbose_name=b'Forwarder (Logistikunternehmen)', blank=True)),
                ('container_no', models.CharField(max_length=255, null=True, verbose_name=b'Containernummer', blank=True)),
                ('seal_no', models.CharField(max_length=255, null=True, verbose_name=b'Plombennummer', blank=True)),
                ('sgs_certified', models.BooleanField(default=False, verbose_name=b'SGS zertifiziert?')),
                ('notes', models.TextField(null=True, verbose_name=b'Bemerkungen zum Container', blank=True)),
                ('organisation_from', models.ForeignKey(blank=True, to='organisation.Organisation', help_text=b'Ort wo der Container geladen wurde.', null=True, verbose_name=b'Verarbeitungspartner')),
            ],
            options={
                'ordering': ['-pickup_date'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name des Landes')),
                ('flag', django_resized.forms.ResizedImageField(help_text=b'Flagge des Landes.', null=True, upload_to=b'velafrica_sud/country/flags/', blank=True)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalContainer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('velos', models.IntegerField(default=0, verbose_name=b'Anzahl Velos')),
                ('velos_worth', models.IntegerField(default=0, verbose_name=b'Wert der Velos')),
                ('spare_parts', models.BooleanField(default=False, verbose_name=b'Ersatzteile transportiert?')),
                ('spare_parts_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('tools_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('various_worth', models.IntegerField(default=0, verbose_name=b'Wert der Ersatzteile')),
                ('pickup_date', models.DateField(verbose_name=b'Ladedatum beim Verarbeitungspartner')),
                ('shipment_date', models.DateField(null=True, verbose_name=b'Verschiffungsdatum ab Europa', blank=True)),
                ('arrival_port_date', models.DateField(null=True, verbose_name=b'Ankunft Hafen Partner', blank=True)),
                ('arrival_partner_date', models.DateField(null=True, verbose_name=b'Ankunft Partner', blank=True)),
                ('logistics', models.CharField(max_length=255, null=True, verbose_name=b'Forwarder (Logistikunternehmen)', blank=True)),
                ('container_no', models.CharField(max_length=255, null=True, verbose_name=b'Containernummer', blank=True)),
                ('seal_no', models.CharField(max_length=255, null=True, verbose_name=b'Plombennummer', blank=True)),
                ('sgs_certified', models.BooleanField(default=False, verbose_name=b'SGS zertifiziert?')),
                ('notes', models.TextField(null=True, verbose_name=b'Bemerkungen zum Container', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('organisation_from', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='organisation.Organisation', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical container',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPartnerSud',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name der Organisation')),
                ('street', models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True)),
                ('plz', models.IntegerField(null=True, verbose_name=b'PLZ', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name=b'Ort', blank=True)),
                ('website', models.CharField(max_length=255, null=True, verbose_name=b'Website', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('country', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='velafrica_sud.Country', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical partner sud',
            },
        ),
        migrations.CreateModel(
            name='PartnerSud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name der Organisation')),
                ('street', models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True)),
                ('plz', models.IntegerField(null=True, verbose_name=b'PLZ', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name=b'Ort', blank=True)),
                ('website', models.CharField(max_length=255, null=True, verbose_name=b'Website', blank=True)),
                ('country', models.ForeignKey(verbose_name=b'Land', to='velafrica_sud.Country')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='historicalcontainer',
            name='partner_to',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='velafrica_sud.PartnerSud', null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='partner_to',
            field=models.ForeignKey(verbose_name=b'Destination', to='velafrica_sud.PartnerSud'),
        ),
    ]
