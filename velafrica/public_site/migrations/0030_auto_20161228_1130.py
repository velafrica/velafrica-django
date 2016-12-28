# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-28 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0029_auto_20161215_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='image',
            field=models.URLField(default='https://placeholdit.imgix.net/~text?txtsize=38&txt=400%C3%97400&w=400&h=400', verbose_name=b'Bild URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partner',
            name='teaserd',
            field=models.BooleanField(default=False, verbose_name=b'Teaser'),
        ),
    ]
