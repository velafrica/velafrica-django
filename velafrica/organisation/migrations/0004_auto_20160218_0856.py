# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_auto_20160202_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(verbose_name=b'Django User Account', to=settings.AUTH_USER_MODEL),
        ),
    ]
