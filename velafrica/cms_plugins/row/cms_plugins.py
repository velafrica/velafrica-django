from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from velafrica.cms_plugins.big_picture.models import BigPicture


class RowPlugin(CMSPluginBase):
    name = _("Row")
    render_template = "cms/plugins/row.html"
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super(RowPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(RowPlugin)