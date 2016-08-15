# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-15 08:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0026_auto_20160810_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contact',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Kontaktperson'),
        ),
        migrations.AlterField(
            model_name='collectionevent',
            name='collection',
            field=models.TextField(blank=True, help_text=b'Infos zur Abholung der Velos', verbose_name=b'Notizen Abtransport'),
        ),
        migrations.AlterField(
            model_name='collectionevent',
            name='notes',
            field=models.TextField(blank=True, help_text=b'Sachen die noch zu erledigen sind / Weitere Infos / Bemerkungen', verbose_name=b'To do'),
        ),
        migrations.AlterField(
            model_name='collectionevent',
            name='processing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_organisation', to='organisation.Organisation', verbose_name=b'Velo Verarbeitung'),
        ),
        migrations.AlterField(
            model_name='collectionevent',
            name='velo_amount',
            field=models.IntegerField(default=0, help_text=b'Anzahl gesammelter Velos', verbose_name=b'Anzahl Velos'),
        ),
    ]
