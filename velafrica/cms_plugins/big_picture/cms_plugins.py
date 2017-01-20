from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from velafrica.cms_plugins.big_picture.models import BigPicture


class BigPicturePlugin(CMSPluginBase):
    model = BigPicture
    name = _("Big Picture")
    render_template = "cms/plugins/big_picture.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super(BigPicturePlugin, self).render(context, instance, placeholder)
        return context

    def copy_relations(self, oldinstance):
    # Because we have a ForeignKey, it's required to copy over
    # the reference from the instance to the new plugin.
        self.picture = oldinstance.picture


plugin_pool.register_plugin(BigPicturePlugin)