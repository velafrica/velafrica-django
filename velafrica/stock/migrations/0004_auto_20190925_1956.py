# Generated by Django 2.1.12 on 2019-09-25 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20190902_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalwarehouse',
            name='organisation',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Die Organisation zu welcher das Lager gehört. (Nur VPN Schweiz Partner)', limit_choices_to={'partnersud': None}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organisation.Organisation', verbose_name='Organisation'),
        ),
        migrations.AlterField(
            model_name='stockchange',
            name='stock_change_type',
            field=models.CharField(choices=[('in', 'in'), ('out', 'out')], max_length=255),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='organisation',
            field=models.ForeignKey(help_text='Die Organisation zu welcher das Lager gehört. (Nur VPN Schweiz Partner)', limit_choices_to={'partnersud': None}, on_delete=django.db.models.deletion.CASCADE, to='organisation.Organisation', verbose_name='Organisation'),
        ),
    ]
