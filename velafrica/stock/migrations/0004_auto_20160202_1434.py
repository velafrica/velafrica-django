# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20160202_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='stock_management',
            field=models.BooleanField(default=False, help_text=b'Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.', verbose_name=b'Automatisches Stock-Management'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='organisation',
            field=models.ForeignKey(verbose_name=b'Organisation', to='organisation.Organisation', help_text=b'Die Organisation zu welcher das Lager geh\xc3\xb6rt.'),
        ),
    ]
