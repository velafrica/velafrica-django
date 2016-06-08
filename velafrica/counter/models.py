# -*- coding: utf-8 -*-
from datetime import timedelta, date
from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation

# Create your models here.
class Entry(models.Model):
    """
    Represents one entry of the velocounter app.
    """
    date = models.DateField(blank=False, null=False, default=timezone.now, verbose_name="Datum")
    organisation = models.ForeignKey(Organisation, blank=False, null=False, verbose_name="Verarbeitsungsort")
    amount = models.IntegerField(blank=False, null=False, verbose_name="Anzahl Velos")
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkungen")
    history = HistoricalRecords()

    @staticmethod
    def get_statistics(id=0):
      """
      Returns a dict with the following keys:
      "org_id": int,
      "velos_today": int,
      "velos_yesterday": int,
      "velos_thisweek": int,
      "velos_thismonth": int,
      "velos_thisyear": int,
      "velos_total": int,
      "velos_max": int,
      "velos_max_date": date,
      "organisations": QuerySet<Organisation>
      """
      statistics = {
        "org_id": id,
        "velos_today": 0,
        "velos_yesterday": 0,
        "velos_thisweek": 0,
        "velos_thismonth": 0,
        "velos_thisyear": 0,
        "velos_total": 0,
        "velos_max": 0,
        "velos_max_date": date.today(),
        "organisations": {}
      }

      entries = Entry.objects.all()

      # get all organisations that already have entries
      org_ids = Entry.objects.order_by().values('organisation').distinct()
      statistics["organisations"] = Organisation.objects.filter(id__in=org_ids)

      if id > 0:
        entries = entries.filter(organisation=org_ids)

      if (entries.count() > 0):
        now = date.today()
        first_day_of_week = now - timedelta(days=now.weekday())

        for entry in entries:
          # sum up total
          statistics["velos_total"] += entry.amount

          # check if it is the biggest amount
          if entry.amount > statistics["velos_max"]:
            statistics["velos_max"] = entry.amount
            statistics["velos_max_date"] = entry.date

          # check if entry is from current year
          if entry.date.year == now.year:
            statistics["velos_thisyear"] += entry.amount

            # check if entry is from current month
            if entry.date.month == now.month:
              statistics["velos_thismonth"] += entry.amount

          # check if entry is from current week
          if entry.date >= first_day_of_week:
            statistics["velos_thisweek"] += entry.amount

          # check if latest entry was from today
          if entry.date == now:
            statistics["velos_today"] += entry.amount

          # get entry from yesterday
          if entry.date == (now - timedelta(days=1)):
            statistics["velos_yesterday"] += entry.amount
        return statistics

    def __unicode__(self):
        return u"{}: {}".format(self.date, self.amount)

    class Meta:
        unique_together = ['organisation', 'date']
        verbose_name_plural = "Entries"
        ordering = ['-date']
