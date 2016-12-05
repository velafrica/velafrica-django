#-*- coding: utf-8 -*-
# Signals for sending automated mails
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from velafrica.sbbtracking.models import TrackingEvent, EmailLog


@receiver(post_save, sender=TrackingEvent)
def send_email(sender, instance, created, **kwargs):
    """
    Send email notification to bicycle donor.
    """
    print "send email"

    # check if the event has been newly created or just updated
    if not created:
        return

    # TODO: set gps default if none has been set

    # set last event on tracking
    instance.tracking.last_event = instance
    #instance.tracking.last_update = instance.datetime
    instance.tracking.save()

    # check if tracking is complete now
    if instance.event_type.complete_tracking:
        instance.tracking.complete = True
        instance.tracking.save()

    if instance.event_type.send_email:

        # check if there is an email on the tracking
        if instance.tracking.email:

            # prepare email fields
            subject = u"Velafrica Velo Tracking {} - {}".format(
                instance.tracking.tracking_no,
                instance.event_type.name
            )
            if instance.event_type.email_text:
                msg_body = u"Hallo {} {},\n\n{}".format(
                    instance.tracking.first_name,
                    instance.tracking.last_name,
                    instance.event_type.email_text
                )

            else:
                msg_body = u"Hallo {} {},\n\nNeuer Velo Tracking Event: {}".format(
                    instance.tracking.first_name,
                    instance.tracking.last_name,
                    instance.event_type.name
                )

            # check if partner info needs to be included and if it is available
            if instance.event_type.show_partner_info and instance.tracking.container:
                partner = instance.tracking.container.partner_to
                msg_body += u"\n\n{}\n{}\n".format(partner.get_name(), partner.get_description())
                if partner.get_website():
                    msg_body += partner.get_website()

            msg_footer = u"Verfolgen Sie Ihr Velo online, auf {}{}\n\nDiese Email wurde automatisch generiert. Bitte antworten Sie nicht darauf.".format(
                getattr(settings, 'APP_URL', 'http://tracking.velafrica.ch'),
                reverse('home:tracking:personal', kwargs={'tracking_no' : instance.tracking.tracking_no})
            )
            msg = u"{}\n\n{}".format(
                msg_body,
                msg_footer
            )
            from_name = getattr(settings, 'EMAIL_FROM_NAME', 'Velafrica Tracking')
            from_email = getattr(settings, 'EMAIL_FROM_EMAIL', 'tracking@velafrica.ch')
            sender = u"{} <{}>".format(from_name, from_email)
            receiver = instance.tracking.email

            # send simple email
            # todo: html email template
            # todo: error handling

            send_mail(subject, msg, sender, [receiver], fail_silently=False)

            # create log entry for email
            log = EmailLog(
                tracking=instance.tracking,
                tracking_event=instance,
                sender=sender,
                receiver=receiver,
                subject=subject,
                message=msg,
                )
            log.save()
