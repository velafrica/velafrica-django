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
		subject = "SBB Tracking {}".format(instance.tracking.tracking_no)
		msg = "New Event: {}".format(instance.event_type.name)
		sender = getattr(settings, 'EMAIL_HOST_USER', 'tracking@velafrica.ch')
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
