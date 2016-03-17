# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import velafrica.core.ftp


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20160316_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=django_resized.forms.ResizedImageField(help_text=b'Product picture.', storage=velafrica.core.ftp.MyFTPStorage(), null=True, upload_to=b'stock/categories/', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(storage=velafrica.core.ftp.MyFTPStorage(), upload_to=b'stock/products/', null=True, verbose_name=b'Produktbild', blank=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='image',
            field=django_resized.forms.ResizedImageField(storage=velafrica.core.ftp.MyFTPStorage(), upload_to=b'stock/warehouses/', null=True, verbose_name=b'Bild des Lagers', blank=True),
        ),
    ]
