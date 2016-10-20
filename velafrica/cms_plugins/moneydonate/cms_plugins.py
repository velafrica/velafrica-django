from cms.plugin_base import CMSPluginBase
from cms.models import CMSPlugin
from cms.plugin_pool import plugin_pool
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Moneydonate
from .admin import MoneydonateAmountInlineAdmin
from .forms import InvoiceForm
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL


class Moneydonate(CMSPluginBase):
    model = Moneydonate
    render_template = "cms/plugins/moneydonate.html"
    name = "Geldspenden"
    inlines = (MoneydonateAmountInlineAdmin,)

    fieldsets = (
        ('Allgemein', {
            'fields': ('title', 'subtitle', 'return_url')
        }),
        ('PayPal', {
            'fields': ('paypal_active', 'paypal_text',)
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
            "notify_url": "https://velafrica-staging-pr-21.herokuapp.com" + reverse('paypal-ipn'),
            "return_url": instance.return_url,
            "cancel_return": "",
            "rm": "1",
            "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
        }
        paypalform = PayPalPaymentsForm(initial=paypal_dict)
        invoiceform = InvoiceForm()

        context.update({
            'amounts': amounts,
            'paypalform': paypalform,
            'invoiceform': invoiceform
        })
        return context


plugin_pool.register_plugin(Moneydonate)
