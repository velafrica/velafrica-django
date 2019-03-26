# -*- coding: utf-8 -*-
from django.db import models

EVENT_TYPES = {
    ('container_created', ''),
    ('container_pickupdate_changed', ''),
    ('container_velos_loaded_changed', ''),
    ('container_velos_unloaded_changed', ''),
    ('container_booked', ''),
    ('warehouse_ride_created', ''),
    ('warehouse_ride_created_bicycles', ''),
    ('warehouse_ride_created_spareparts', ''),
    ('warehouse_stockchange_in_created'),
    ('warehouse_stockchange_out_created'),
}

class EventListener(models.Model):
    """
    TODO: everything
    - define types
    - unsubscribe per user per object
    - sending: instantly vs summary at end of day
    """

    #type = ""
    #users
    #groups
    #custom_emails
    #object_ids # None = all


    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
