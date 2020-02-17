# -*- coding: utf-8 -*-
import datetime
import os
import uuid

from django.db.models import Max
from django.urls import reverse
from django_resized import ResizedImageField
from velafrica.core.storage import MyStorage
from velafrica.stock.models import Warehouse
from velafrica.velafrica_sud.models import Container

from django.db import models
from .settings import BIKE_TYPES

fs = MyStorage()


# image path and name
def bike_images(instance, filename):
    return 'bike_img/{}_{}'.format(
        instance.id,
        filename
    )


# get the next number for A+-Bikes
def next_a_plus_number():
    return Bike.objects.aggregate(new_number=Max('number')+1)['new_number']


# generates a unique id with the year as prefix
def bike_id():
    return datetime.datetime.now().strftime('%y') + "-" + uuid.uuid4().hex[:6].upper()


class BikeCategory(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Category',
        default='',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "bike categories"


class BikeStatus:
    NORMAL = 0
    DISMISSED = 1


class Bike(models.Model):
    id = models.CharField(primary_key=True, unique=True, default=bike_id, max_length=255)

    # bike category
    type = models.CharField(choices=BIKE_TYPES, null=True, max_length=255, verbose_name=u"Type")
    category = models.ForeignKey(
        BikeCategory,
        null=True,
        verbose_name=u"Type",
        on_delete=models.CASCADE,
    )

    # production signature
    date = models.DateField(default=datetime.date.today, verbose_name=u"Date")
    visa = models.CharField(max_length=255, blank=True, verbose_name=u"Visa")

    # placement of the bike
    warehouse = models.ForeignKey(
        Warehouse,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=u"Warehouse",
    )

    # A+
    a_plus = models.BooleanField(default=False, verbose_name=u"A+")
    number = models.IntegerField(unique=True, default=next_a_plus_number, editable=True, verbose_name=u"No.")

    # Details
    brand = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Brand")
    bike_model = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Model")
    gearing = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Group of components")
    drivetrain = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Drivetrain")
    brake = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Brake")
    colour = models.CharField(max_length=255, default="", blank=True, verbose_name=u"Colour")
    size = models.CharField(max_length=255, default='', blank=True, verbose_name=u"Size")
    suspension = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Suspension")
    rear_suspension = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"Rear Suspension")
    extraordinary = models.TextField(max_length=255, null=True, blank=True, verbose_name=u"Extraordinary")
    status = models.IntegerField(
        default=0,
        verbose_name='status',
        choices=[
            (0, 'Normal'),
            (1, 'Dismissed'),
        ],
        help_text="Dismissed = bike is neither in stock nor sold."
    )

    # image(s)
    image = ResizedImageField(
        storage=fs,
        size=[1920, 1080],
        upload_to=bike_images,
        blank=True,
        null=True,
        verbose_name=u"Image",
    )

    # Shipping
    container = models.ForeignKey(
        Container,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=u"Container",
    )

    # Metadata
    date_created = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateField(auto_now=True, null=True)

    def __str__(self):
        if self.number:
            return '#{} - {}'.format(self.number, self.category)
        return '{} - {}'.format(self.id, self.category)

    # backend url
    def get_backend_url(self):
        return reverse("admin:bikes_bike_change", args=[self.pk])

    class Meta:
        ordering = ["-number"]


# The following auto-delete files from filesystem when they are unneeded:
def delete_file(filename):
    if os.path.isfile(filename):
        folder = os.path.dirname(filename)
        os.remove(filename)
        try:
            os.rmdir(folder)
        except OSError:
            return

# TODO: 'auto_file_deletion' witch would work with AWS
# temporary workaround - no deletion :)

# @receiver(models.signals.post_delete, sender=Bike)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.image:
#         delete_file(instance.image.path)
#
#
# @receiver(models.signals.pre_save, sender=Bike)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = Bike.objects.get(pk=instance.pk).image
#     except Bike.DoesNotExist:
#         return False
#
#     new_file = instance.image
#     if not old_file == new_file:
#         if old_file.name:
#             delete_file(old_file.path)
#
