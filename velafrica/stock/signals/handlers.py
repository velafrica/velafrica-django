# Signals for sending automated mails
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from velafrica.stock.models import StockTransfer

# TODO: define signals for booking / revoking StockTransfers
