# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, max_length=7, null=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Must be a hexcode (e.g. #000 or #000000)', code=b'invalid_hexcode')]),
        ),
        migrations.AddField(
            model_name='historicalcategory',
            name='color',
            field=models.CharField(blank=True, max_length=7, null=True, help_text=b'Colour code to use for this category (hex value, i.e. #000 or #000000)', validators=[django.core.validators.RegexValidator(regex=b'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message=b'Must be a hexcode (e.g. #000 or #000000)', code=b'invalid_hexcode')]),
        ),
    ]
