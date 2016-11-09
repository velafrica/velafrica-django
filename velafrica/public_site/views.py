# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import get_template
from paypal.standard.forms import PayPalPaymentsForm
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL, GMAP_API_KEY, INVOICE_ORDER_RECEIVER
from .forms import InvoiceForm
from .models import DonationAmount

def render_template(request):
    template_name = '/index'
    if request.path != '/':
        template_name = request.path

    return render_to_response('public_site' + template_name + '.html', {

    }, context_instance=RequestContext(request))


def render_map_template(request):
    template_name = 'public_site/map.html'
    template_context = {
        'nofooter': True,
        'api_key': GMAP_API_KEY,
        'map_data_url': reverse('api:public:dropoffs')
    }

    if 'search' in request.GET:
        template_context.update({
            'search': request.GET['search']
        })

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_donation_template(request):
    template_name = 'public_site/donation.html'
    donation_amounts = DonationAmount.objects.filter(is_active=True).order_by('amount')
    paypal_dict = {
        "business": PAYPAL_RECEIVER_MAIL,
        "amount": donation_amounts.first().amount,
        "currency_code": "CHF",
        "item_name": "Velafrica Donation",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url":  request.build_absolute_uri(reverse('home:donation:thank_you_paypal')),
        "cancel_return": request.build_absolute_uri(),
        "rm": "1",
        "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }
    paypalform = PayPalPaymentsForm(initial=paypal_dict)
    invoiceform = InvoiceForm()
    template_context = {
        'amounts': donation_amounts,
        'paypalform': paypalform,
        'invoiceform': invoiceform
    }

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_walkthrough_template(request):
    template_name = 'public_site/walkthrough.html'

    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def order_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoiceorder = form.save()

            email_context = {
                'firstname': form.cleaned_data['first_name'],
                'lastname': form.cleaned_data['last_name'],
                'address': u"{}, {}".format(form.cleaned_data['address'], form.cleaned_data['zip']),
                'comment': form.cleaned_data['comment'],
                'number_invoices': form.cleaned_data['number_invoices'],
                'donation_amount': form.cleaned_data['donation_amount'],
                'url': request.build_absolute_uri(reverse('admin:public_site_invoiceorder_change', args=[invoiceorder.pk])),
            }

            subject = 'Neue ESR Bestellung'
            content = get_template('email/invoice_order.txt').render(email_context)
            # copied from tracking handlers
            from_name = getattr(settings, 'EMAIL_FROM_NAME', 'Velafrica Tracking')
            from_email = getattr(settings, 'EMAIL_FROM_EMAIL', 'tracking@velafrica.ch')
            sender = u"{} <{}>".format(from_name, from_email)

            send_mail(subject, content, sender, [INVOICE_ORDER_RECEIVER], fail_silently=False)
            return redirect(form.cleaned_data['invoice_redirect_url'])
        else:
            # TODO: track error with rollbar
            return redirect('/')


def thank_you(request):
    template_name = 'public_site/donation-thank-you.html'
    return render_to_response(template_name, {}, context_instance=RequestContext(request))

def thank_you_paypal(request):
    template_name = 'public_site/donation-thank-you.html'
    return render_to_response(template_name, {'paypal': True}, context_instance=RequestContext(request))
