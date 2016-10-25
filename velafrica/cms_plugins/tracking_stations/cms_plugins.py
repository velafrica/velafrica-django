from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from velafrica.sbbtracking.models import Tracking
from .models import TrackingStation, TrackingStationQuery
from .admin import TrackingStationQueryInlineAdmin
from django.utils.translation import ugettext_lazy as _


class HelloPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "cms/plugins/test.html"
    cache = False


class TrackingStations(CMSPluginBase):
    model = TrackingStation
    render_template = "cms/plugins/tracking_stations.html"
    name = "Tracking Stationen"
    inlines = (TrackingStationQueryInlineAdmin,)

    def render(self, context, instance, placeholder):
        context = super(TrackingStations, self).render(context, instance, placeholder)
        queries = instance.queries.all()

        # for query in queries:
        #     count = -1
        #
        #     for event_type in query.event_types.all():
        #         count += Tracking.objects.all().filter(last_event__event_type_id=event_type.id).count()
        #
        #     query.count = count

        context.update({
            'queries': queries
        })
        return context


plugin_pool.register_plugin(TrackingStations)
