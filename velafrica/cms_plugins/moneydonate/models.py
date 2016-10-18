# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from django.db import models


class Moneydonate(CMSPlugin):
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='+',
        parent_link=True
    )

    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    paypal_active = models.BooleanField(verbose_name='PayPal aktiv')
    paypal_text = models.TextField(blank=True, verbose_name='Beschreibung PayPal')
    paypal_cancel_url = models.URLField(verbose_name='Abbruch URL', blank=True)
    paypal_return_url = models.URLField(verbose_name='Weiterleitungsadresse', blank=True)

    onba_active = models.BooleanField(verbose_name='E-Banking aktiv')
    onba_text = models.TextField(max_length=255, blank=True, verbose_name='Beschreibung E-Banking')
    onba_account = models.CharField(max_length=255, blank=True, verbose_name='Kontonummer')
    onba_recipient = models.CharField(max_length=255, blank=True, verbose_name='Empfänger')
    onba_iban = models.CharField(max_length=255, blank=True, verbose_name='IBAN')
    onba_bic = models.CharField(max_length=255, blank=True, verbose_name='BIC')

    invoice_active = models.BooleanField(verbose_name='Einzahlungsschein aktiv')
    invoice_text = models.TextField(max_length=255, blank=True, verbose_name='Beschreibung Einzahlungsschein')

    def copy_relations(self, old_instance):
        for amount in old_instance.amounts.all():
            amount.pk = None
            amount.plugin = self
            amount.save()


class MoneydonateAmount(models.Model):
    plugin = models.ForeignKey(Moneydonate, related_name='amounts')
    description = models.CharField(max_length=255, verbose_name='Beschreibung')
    amount = models.IntegerField(verbose_name='Betrag')
    is_active = models.BooleanField(default=True, verbose_name='Aktiv')

    class Meta:
        verbose_name = 'Geldspendebeträge'
        verbose_name = 'Geldspendebeträge'
