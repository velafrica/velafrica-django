from cms.models.pluginmodel import CMSPlugin
from django.db import models
from velafrica.sbbtracking.models import TrackingEventType, Tracking


def get_event_types_as_choice():
    tracking_event_types = TrackingEventType.objects.all()
    ret_types = []
    for event_type in tracking_event_types:
        ret_types.append((event_type.id, event_type.name))

    return ret_types


class TrackingStation(CMSPlugin):

    # had to do this, otherwise it will end up in a migration conflict/error
    # read more here: https://www.django-cms.org/en/blog/2016/03/03/announcing-support-for-django-19/
    # under *Important Issues Arise When Using Django 1.9
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='+',
        parent_link=True
    )

    def get_tracking_types(self):
        return get_event_types_as_choice()

    def copy_relations(self, old_instance):
        for query in old_instance.queries.all():
            query.pk = None
            query.plugin = self
            query.save()
         
        # for query in old_instance.queries.all():
        #     for event_type in query.event_types.all():
        #         event_type.pk = None
        #         event_type.query = query
        #         event_type.save()


class TrackingStationQuery(models.Model):

    label = models.CharField(max_length=255, verbose_name="Label")
    # TODO: find better solution!
    #event_types = MultiSelectField(choices=lazy(get_event_types_as_choice, list)())
    event_types = models.ManyToManyField(TrackingEventType, related_name='tracking_station_queries')
    # event_types = models.CharField(max_length=255, verbose_name="Event Typen")

    query_order = models.IntegerField(verbose_name="Reihenfolge", default=0)
    plugin = models.ForeignKey(
        TrackingStation,
        related_name="queries"
    )

    def get_count(self):
        count = -1
        for event_type in self.event_types.all():
            count += Tracking.objects.all().filter(last_event__event_type_id=event_type.id).count()
            # count =
            # count += 1

        return count

