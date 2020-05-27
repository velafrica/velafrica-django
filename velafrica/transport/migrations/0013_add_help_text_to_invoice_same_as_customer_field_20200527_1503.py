# Generated by Django 2.1.15 on 2020-05-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0012_textfield_type_for_all_notes_and_comments_20200527_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalride',
            name='invoice_same_as_customer',
            field=models.BooleanField(default=True, help_text='Standardmässig wird als Rechnungsempfänger die Adresse des Kunden (Auftraggeber) verwendet.', verbose_name='Rechnungsadresse = Kundenadresse'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='invoice_same_as_customer',
            field=models.BooleanField(default=True, help_text='Standardmässig wird als Rechnungsempfänger die Adresse des Kunden (Auftraggeber) verwendet.', verbose_name='Rechnungsadresse = Kundenadresse'),
        ),
    ]
