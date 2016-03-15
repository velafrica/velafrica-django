# Signals for sending automated mails
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from velafrica.sbbtracking.models import TrackingEvent, EmailLog

@receiver(post_save, sender=TrackingEvent)
def send_email(sender, instance, **kwargs):
	"""
	"""
	
	print("Sending email")

	# prepare email fields
	subject = "SBB Tracking {}".format(instance.tracking.tracking_no)
	msg = 'Here is the message.'
	sender = 'velos4africa@gmail.com'
	receiver = instance.tracking.email

	# send simple email
	# todo: html email template
	send_mail(subject, msg, sender, [receiver], fail_silently=False)

	# create log entry for email
	log = EmailLog(
		tracking=instance.tracking,
		sender=sender,
		receiver=receiver,
		subject=subject,
		message=msg,
		)
	log.save()
