# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class ApiUser(models.Model):
    """
    ApiUser needs to be created for every user that should get permission to authenticate on the api.
    """
    user = models.ForeignKey(User)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        status = ""
        if self.active:
            status = " (inactive)"
        return u"{}{}".format(self.user, status)
