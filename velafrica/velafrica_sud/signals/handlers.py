#-*- coding: utf-8 -*-
# Signals for sending automated mails
from django.db.models.signals import post_save
from django.dispatch import receiver

from velafrica.velafrica_sud.models import Container


@receiver(post_save, sender=Container)
def calc_time_to_customer(sender, instance, created, **kwargs):
    """
    Calculate transport time.
    """
    if instance.arrival_partner_date:
        delta = instance.calc_time_to_customer()
        if delta != instance.time_to_customer:
            instance.time_to_customer = delta
            instance.save()

    elif instance.time_to_customer:
        instance.time_to_customer = None
        instance.save()