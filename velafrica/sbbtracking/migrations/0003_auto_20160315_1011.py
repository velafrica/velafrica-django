# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0008_auto_20160310_1432'),
        ('sbbtracking', '0002_auto_20160315_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltracking',
            name='plz',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='street',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='tel',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='town',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='plz',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='street',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='tel',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='town',
        ),
        migrations.AddField(
            model_name='historicaltracking',
            name='container',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='velafrica_sud.Container', null=True),
        ),
        migrations.AddField(
            model_name='tracking',
            name='container',
            field=models.ForeignKey(blank=True, to='velafrica_sud.Container', null=True),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='completed',
            field=models.BooleanField(default=False, verbose_name=b'Velo ist in Afrika angekommen'),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='number_of_velos',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos'),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='ready_for_export',
            field=models.BooleanField(default=False, verbose_name=b'Velo ist exportbereit'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='completed',
            field=models.BooleanField(default=False, verbose_name=b'Velo ist in Afrika angekommen'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='number_of_velos',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='ready_for_export',
            field=models.BooleanField(default=False, verbose_name=b'Velo ist exportbereit'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='vpn',
            field=models.ForeignKey(blank=True, to='organisation.Organisation', help_text=b'wird momentan noch nicht ber\xc3\xbccksichtigt', null=True, verbose_name=b'Partner'),
        ),
    ]
