# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from paypal.standard.forms import PayPalPaymentsForm
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL

def render_template(request):
    template_name = '/index'
    template_context = {}
    if request.path != '/':
        template_name = request.path

        # donation templates need more context data (like paypal form, invoice form and stuff)
        if request.path == '/donation':
            paypal_dict = {
                "business": PAYPAL_RECEIVER_MAIL,
                # "amount": amounts.first().amount,
                "currency_code": "CHF",
                "item_name": "Velafrica Donation",
                "invoice": "unique-invoice-id",
                "notify_url": "https://velafrica-staging-pr-21.herokuapp.com" + reverse('paypal-ipn'),
                "return_url": '', # TODO: return url
                "cancel_return": "",
                "rm": "1",
                "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
            }
            paypalform = PayPalPaymentsForm(initial=paypal_dict)

            template_context.update({
                'paypalform': paypalform
            })

    return render_to_response('public_site' + template_name + '.html', template_context, context_instance=RequestContext(request))
