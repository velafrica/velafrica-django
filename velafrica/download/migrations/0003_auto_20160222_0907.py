# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_auto_20160222_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='file',
            name='category',
            field=models.ForeignKey(blank=True, to='download.Category', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcategory',
            name='name',
            field=models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Name'),
        ),
    ]
