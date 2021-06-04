# Generated by Django 2.1.15 on 2020-08-04 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('transport', '0014_change_verbose_names_of_velo_amount_fields_20200723_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalride',
            name='co_driver',
            field=models.ForeignKey(blank=True, db_constraint=False,
                                    help_text='Nur anzugeben falls noch ein Beifahrer dabei war.', null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                    to='transport.Driver', verbose_name='Beifahrer'),
        ),
        migrations.AddField(
            model_name='ride',
            name='co_driver',
            field=models.ForeignKey(blank=True, help_text='Nur anzugeben falls noch ein Beifahrer dabei war.',
                                    null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='co_driver',
                                    to='transport.Driver', verbose_name='Beifahrer'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(blank=True, help_text='Person die den Transport durchgeführt hat.', null=True,
                                    on_delete=django.db.models.deletion.SET_NULL, to='transport.Driver',
                                    verbose_name='Fahrer'),
        ),
    ]