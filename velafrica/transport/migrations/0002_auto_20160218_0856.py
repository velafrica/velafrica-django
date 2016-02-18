# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ride',
            options={'ordering': ['-date', 'from_warehouse']},
        ),
    ]
