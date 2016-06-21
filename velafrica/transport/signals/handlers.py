#-*- coding: utf-8 -*-
# Signals for sending automated mails
from datetime import datetime
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from velafrica.transport.models import Ride
from velafrica.stock.models import Warehouse

@receiver(post_save, sender=Ride)
def send_email(sender, instance, created, **kwargs):
    """
    Send email notification to bicycle donor.
    """

    print "post save ride"

    # check if the event has been newly created or just updated
    if not created:
        return

    warehouse = instance.to_warehouse

    emails = warehouse.notify_on_incoming_transport
    receiver_list = []

    if instance.spare_parts:
        if emails:
            for line in emails.splitlines():
                try:
                    validate_email(line)
                except ValidationError as e:
                    print "oops! no email {}".format(line)
                else:
                    print "hooray! email is valid, notify {}".format(line)
                    receiver_list += [line]
    if receiver:
        subject = "Neue Ersatzteile in {}".format(warehouse)

        r = 'admin:{}_{}_change'.format(instance._meta.app_label, instance._meta.model_name)
        admin_url = reverse(r, args=[instance.id])

        msg = "Eine neue Lieferung vom Transport ist soeben im Lager {} eingetroffen.\n\nDatum: {}\nFahrer: {}\nHerkunft: {}\nBemerkungen: {}\n\nFahrt anschauen: <a href='{}'>".format(warehouse, instance.date, instance.driver, instance.from_warehouse, instance.note, admin_url)
        from_name = getattr(settings, 'EMAIL_FROM_NAME', 'Velafrica Tracking')
        from_email = getattr(settings, 'EMAIL_FROM_EMAIL', 'tracking@velafrica.ch')
        sender = u"{} <{}>".format(from_name, from_email)
        send_mail(subject, msg, sender, receiver_list, fail_silently=False)
