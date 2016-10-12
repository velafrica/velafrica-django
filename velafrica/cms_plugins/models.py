from cms.models.pluginmodel import CMSPlugin
from django.db import models
from velafrica.sbbtracking.models import TrackingEventType, TrackingEvent


class TrackingStationQuery(models.Model):
    pass


class TrackingStation(CMSPlugin):

    def get_tracking_types(self):
        tracking_types = TrackingEventType.objects.all()
        ret_types = {}
        for tt in tracking_types:
            ret_types[tt.name] = TrackingEvent.objects.filter(event_type=tt).count()

        return ret_types


    loop_times = range(1, 7)
