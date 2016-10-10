# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0008_auto_20160310_1432'),
        ('organisation', '0004_auto_20160218_0856'),
        ('sbbtracking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltrackingeventstate',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltrackingevent',
            name='state',
        ),
        migrations.RemoveField(
            model_name='trackingevent',
            name='state',
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='destination',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='velafrica_sud.PartnerSud', null=True),
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='ready_for_export',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='vpn',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='organisation.Organisation', null=True),
        ),
        migrations.AddField(
            model_name='historicaltrackingevent',
            name='event_type',
            field=models.CharField(default=b'initial', help_text=b'Art des Events', max_length=255, choices=[(b'initial', b'Tracking erstellt'), (b'vpn_in', b'Eingang VPN'), (b'workshop_in', b'Eingang Werkstatt'), (b'ready_for_export', b'Bereit f\xc3\xbcr Export'), (b'load_container', b'Containerverlad'), (b'arrival', b'Ankunft Partner S\xc3\xbcd')]),
        ),
        migrations.AddField(
            model_name='tracking',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tracking',
            name='destination',
            field=models.ForeignKey(verbose_name=b'Destination', blank=True, to='velafrica_sud.PartnerSud', null=True),
        ),
        migrations.AddField(
            model_name='tracking',
            name='ready_for_export',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tracking',
            name='vpn',
            field=models.ForeignKey(verbose_name=b'Partner', blank=True, to='organisation.Organisation', null=True),
        ),
        migrations.AddField(
            model_name='trackingevent',
            name='event_type',
            field=models.CharField(default=b'initial', help_text=b'Art des Events', max_length=255, choices=[(b'initial', b'Tracking erstellt'), (b'vpn_in', b'Eingang VPN'), (b'workshop_in', b'Eingang Werkstatt'), (b'ready_for_export', b'Bereit f\xc3\xbcr Export'), (b'load_container', b'Containerverlad'), (b'arrival', b'Ankunft Partner S\xc3\xbcd')]),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='town',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Stadt', blank=True),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='town',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Stadt', blank=True),
        ),
        migrations.DeleteModel(
            name='HistoricalTrackingEventState',
        ),
        migrations.DeleteModel(
            name='TrackingEventState',
        ),
    ]
