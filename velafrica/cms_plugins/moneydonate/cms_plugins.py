from cms.plugin_base import CMSPluginBase
from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Moneydonate
from .admin import MoneydonateAmountInlineAdmin
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL


class Moneydonate(CMSPluginBase):
    model = Moneydonate
    render_template = "cms/plugins/moneydonate.html"
    name = "Geldspenden"
    inlines = (MoneydonateAmountInlineAdmin,)

    fieldsets = (
        ('Allgemein', {
            'fields': ('title', 'subtitle',)
        }),
        ('PayPal', {
            'fields': ('paypal_active', 'paypal_text',
                       'paypal_return_url', 'paypal_cancel_url',)
        }),
        ('E-Banking', {
            'fields': ('onba_active', 'onba_text', 'onba_account',
                       'onba_recipient', 'onba_iban', 'onba_bic',),
        }),
        ('Einzahlungsschein', {
            'fields': ('invoice_active', 'invoice_text',),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(Moneydonate, self).render(context, instance, placeholder)
        amounts = instance.amounts.filter(is_active=True).order_by('amount')

        paypal_dict = {
            "business": PAYPAL_RECEIVER_MAIL,
            "amount": amounts.first().amount,
            "currency_code": "CHF",
            "item_name": "Velafrica Donation",
            "invoice": "unique-invoice-id",
            "notify_url": "https://5dacf3f3.eu.ngrok.io" + reverse('paypal-ipn'),
            "return_url": instance.paypal_return_url,
            "cancel_return": instance.paypal_cancel_url,
            "rm": "1",
            "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
        }
        form = PayPalPaymentsForm(initial=paypal_dict)

        context.update({
            'amounts': amounts,
            'form': form
        })
        return context


plugin_pool.register_plugin(Moneydonate)
