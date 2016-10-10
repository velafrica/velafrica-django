from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class HelloPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "cms/plugins/test.html"
    cache = False

class TrackingStations(CMSPluginBase):
    model = CMSPlugin
    render_template = "cms/plugins/tracking_stations.html"
    name = "Tracking Stationen"

plugin_pool.register_plugin(HelloPlugin)
plugin_pool.register_plugin(TrackingStations)
