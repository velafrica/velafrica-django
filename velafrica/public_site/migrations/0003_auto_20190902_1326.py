# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-02 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0002_contactrequest_content_event_eventdatetime_partner_references_sbbticketorder_supporter_teammember_wa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='email',
            field=models.CharField(max_length=255, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='note',
            field=models.TextField(verbose_name='Nachricht'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='content',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='content',
            name='key',
            field=models.CharField(max_length=255, verbose_name='Key'),
        ),
        migrations.AlterField(
            model_name='content',
            name='language',
            field=models.CharField(max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='content',
            name='path',
            field=models.CharField(max_length=255, verbose_name='Pfad'),
        ),
        migrations.AlterField(
            model_name='content',
            name='value',
            field=models.TextField(blank=True, verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='donationamount',
            name='description',
            field=models.TextField(verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='donationamount',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktiv'),
        ),
        migrations.AlterField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Aktiv'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pub_event_address', to='organisation.Address', verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pub_event_category', to='collection.EventCategory', verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(blank=True, max_length=255, verbose_name='Veranstalter'),
        ),
        migrations.AlterField(
            model_name='eventdatetime',
            name='date',
            field=models.DateField(verbose_name='Datum'),
        ),
        migrations.AlterField(
            model_name='eventdatetime',
            name='time_end',
            field=models.CharField(blank=True, max_length=255, verbose_name='Bis'),
        ),
        migrations.AlterField(
            model_name='eventdatetime',
            name='time_start',
            field=models.CharField(blank=True, max_length=255, verbose_name='Von'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Anmerkung'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='donation_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Betrag'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='empty_invoice',
            field=models.BooleanField(default=False, verbose_name='Leerer Einzahlungsschein'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='number_invoices',
            field=models.IntegerField(default=1, verbose_name='Menge'),
        ),
        migrations.AlterField(
            model_name='invoiceorder',
            name='zip',
            field=models.CharField(max_length=255, verbose_name='PLZ, Ort'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='category',
            field=models.CharField(blank=True, max_length=255, verbose_name='Kategorie/Bereich'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='city',
            field=models.CharField(max_length=255, verbose_name='Stadt'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='country',
            field=models.IntegerField(choices=[(1, 'Afrika'), (2, 'Schweiz')], verbose_name='Land'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='image',
            field=models.URLField(verbose_name='Bild URL'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='link',
            field=models.CharField(blank=True, max_length=255, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Kanton/Staat'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='teaserd',
            field=models.BooleanField(default=False, verbose_name='Teaser'),
        ),
        migrations.AlterField(
            model_name='references',
            name='image',
            field=models.CharField(max_length=255, verbose_name='Bild-URL'),
        ),
        migrations.AlterField(
            model_name='references',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='references',
            name='sorting',
            field=models.IntegerField(default=0, verbose_name='Sortierung'),
        ),
        migrations.AlterField(
            model_name='references',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Strasse und Hausnummer'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='Anzahl'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='email',
            field=models.CharField(max_length=255, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='note',
            field=models.TextField(blank=True, verbose_name='Bemerkung'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='sbbticketorder',
            name='zip',
            field=models.CharField(max_length=255, verbose_name='PLZ und Ort'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Aktiv'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='description',
            field=models.CharField(blank=True, help_text='Max. 140 Zeichen', max_length=140, verbose_name='Kurzbeschreibung'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='image',
            field=models.CharField(blank=True, max_length=255, verbose_name='Bild/Logo URL'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='link',
            field=models.URLField(verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='supporter',
            name='sorting',
            field=models.IntegerField(default=0, verbose_name='Sortierung'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='email',
            field=models.CharField(blank=True, max_length=255, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=models.CharField(blank=True, max_length=255, verbose_name='Bild-URL'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='position',
            field=models.CharField(blank=True, max_length=255, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='sorting',
            field=models.IntegerField(default=0, verbose_name='Sortierung'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='address_note',
            field=models.TextField(blank=True, verbose_name='Standortbeschreibung'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='can_deliver',
            field=models.BooleanField(default=False, verbose_name='Kann Abtransport zu Partner übernehmen'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='can_store',
            field=models.BooleanField(default=False, verbose_name='Kann Velos vor Ort zwischenlagern'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='collected_before',
            field=models.BooleanField(default=False, verbose_name='Bereits für Velafrica gesammelt'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='collected_before_note',
            field=models.TextField(blank=True, verbose_name='Wann und wo'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Datum'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='date_fixed',
            field=models.BooleanField(default=False, verbose_name='Datum fixiert'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='email',
            field=models.CharField(max_length=255, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='expected_velos',
            field=models.IntegerField(choices=[(1, '1 - 20'), (2, '21 - 50'), (3, '51 - 100'), (4, '101 - 1000'), (5, '> 1000')], default=1, verbose_name='Erwartete Menge gesammelter Velos'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='organizer_type',
            field=models.IntegerField(choices=[(1, 'Verein'), (2, 'Firma'), (3, 'Gemeinde'), (4, 'Kirchgemeinde'), (5, 'Schule'), (6, 'Liegenschaftsverwaltung'), (7, 'Privatperson'), (8, 'Andere')], default=1, verbose_name='Veranstalter'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='pickup_time_end',
            field=models.CharField(blank=True, max_length=255, verbose_name='Annahmezeit bis'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='pickup_time_start',
            field=models.CharField(blank=True, max_length=255, verbose_name='Annahmezeit von'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='responsible_email',
            field=models.CharField(blank=True, max_length=255, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='responsible_first_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='responsible_last_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='responsible_phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='supporter_count',
            field=models.IntegerField(choices=[(1, '1 - 10'), (2, '11 - 20'), (3, '21 - 30'), (4, '31 - 40'), (4, '41 - 50')], default=1, verbose_name='Anzahl Helfer'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='supporter_note',
            field=models.TextField(blank=True, verbose_name='Bemerkung'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='velafrica_pickup',
            field=models.BooleanField(default=False, verbose_name='Abtransport durch Velafrica'),
        ),
        migrations.AlterField(
            model_name='walkthroughrequest',
            name='zip',
            field=models.CharField(blank=True, max_length=255, verbose_name='Postleitzahl'),
        ),
    ]