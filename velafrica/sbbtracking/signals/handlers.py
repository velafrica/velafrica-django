#-*- coding: utf-8 -*-
# Signals for sending automated mails
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from velafrica.sbbtracking.models import TrackingEvent, EmailLog

@receiver(post_save, sender=TrackingEvent)
def send_email(sender, instance, **kwargs):
	"""
	"""

	if instance.event_type.send_email:

		# prepare email fields
		subject = u"Velafrica Velo Tracking {} - {}".format(
			instance.tracking.tracking_no, 
			instance.event_type.name
		)
		if instance.event_type.email_text:
			msg_header = u"Hallo {} {},\n\n{}".format(
				instance.tracking.first_name,
				instance.tracking.last_name,
				instance.event_type.email_text
			)
		else:
			msg_header = u"Hallo {} {},\n\nNeuer Velo Tracking Event: {}".format(
				instance.tracking.first_name,
				instance.tracking.last_name,
				instance.event_type.name
			)

		msg_footer = u"Verfolgen Sie Ihr Velo online, auf http://tracking.velafrica.ch/tracking/{}\n\nDiese Email wurde automatisch generiert. Bitte antworten Sie nicht darauf.".format(
			instance.tracking.tracking_no
		)
		msg = u"{}\n\n{}".format(
			msg_header,
			msg_footer
		)
		from_name = getattr(settings, 'EMAIL_FROM_NAME', 'Velafrica Tracking')
		from_email = getattr(settings, 'EMAIL_FROM_EMAIL', 'tracking@velafrica.ch')
		sender = u"{} <{}>".format(from_name, from_email)
		receiver = instance.tracking.email

		# send simple email
		# todo: html email template
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
