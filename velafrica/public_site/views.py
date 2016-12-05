# -*- coding: utf-8 -*-
import collections
from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from paypal.standard.forms import PayPalPaymentsForm
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL, GMAP_API_KEY, ORDER_RECEIVER
from velafrica.core.utils import send_mail
from velafrica.collection.models import Dropoff
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType
from .forms import InvoiceForm, SbbTicketOrderForm, WalkthroughRequestForm
from .models import DonationAmount, WalkthroughRequest, TeamMember, References, Partner

def render_template(request):
    template_name = '/index'
    template_context = {}
    if request.path != '/':
        template_name = request.path

    if request.path == '/':
        template_context['velo_count'] = Tracking.get_tracked_velo_count()

    return render_to_response('public_site' + template_name + '.html', template_context, context_instance=RequestContext(request))


def render_map_template(request):
    template_name = 'public_site/map.html'
    template_context = {
        'nofooter': True,
        'api_key': GMAP_API_KEY,
        'map_data_url': reverse('api:public:dropoffs'),
        'sbb_ticket_order_url': reverse('home:sbbticket')
    }

    if request.user.is_authenticated():
        template_context['auth'] = True;

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


def render_sbb_ticker_order(request):
    template_name = 'public_site/sbb_ticket_order.html'
    template_context = {
        'form': SbbTicketOrderForm(),
        'donation_url': reverse('home:donation:home')
    }

    if 'id' in request.GET:
        dropoff = Dropoff.objects.get(id=int(request.GET['id']))
        if dropoff:
            template_context.update({'dropoff': dropoff})
    else:
        dropoff = None

    if request.method == 'POST':
        form = SbbTicketOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.dropoff = dropoff
            order.save()

            email_context = {
                'dropoff': dropoff,
                'firstname': order.first_name,
                'lastname': order.last_name,
                'amount': order.amount,
                'address': u"{}, {}".format(order.address, order.zip),
                'email': order.email,
                'phone': order.phone,
                'note': order.note,
                'url': request.build_absolute_uri(reverse('admin:public_site_sbbticketorder_change', args=[order.pk]))
            }

            subject = 'Neue SBB Ticket Bestellung'

            send_mail('email/sbb_ticket_order.txt', subject, [ORDER_RECEIVER], email_context)

            template_context['success'] = True
        else:
            template_context['form'] = form

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_walkthrough_template(request):
    template_name = 'public_site/walkthrough.html'
    template_context = {
        'form': WalkthroughRequestForm()
    }

    partials = {
        'collection': 'public_site/partials/walkthroughs/collectionpoint.html',
        'company': 'public_site/partials/walkthroughs/company.html',
        'school': 'public_site/partials/walkthroughs/school.html',
        'voluntary': 'public_site/partials/walkthroughs/voluntary.html'
    }

    template_context.update({
         'partial': partials.get(resolve(request.path).url_name, 'nothing')
    })

    if request.method == 'POST':
        form = WalkthroughRequestForm(request.POST)
        if form.is_valid():
            walkthrough = form.save()

            email_context = {
                'data': walkthrough,
                'url': request.build_absolute_uri(reverse('admin:public_site_walkthroughrequest_change', args=[walkthrough.pk])),
            }

            subject = 'Neue Sammelanlassanfrage'
            send_mail('email/walkthrough_request.txt', subject, [ORDER_RECEIVER], email_context)
            template_name = 'public_site/walkthrough-send.html'
        else:
            template_context['form'] = form

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


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

            send_mail('email/invoice_order.txt', subject, [ORDER_RECEIVER], email_context)
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


def render_about_us_template(request):
    template_name = 'public_site/ueber-uns.html'
    template_context = {}

    if References.objects.count() > 0:
        template_context.update({
            'references': References.objects.filter(active=True).order_by('-sorting')
        })

    if TeamMember.objects.count() > 0:
        template_context.update({
            'team': TeamMember.objects.filter(active=True).order_by('-sorting')
        })

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_personal_tracking(request, tracking_no=''):
    template_name = 'public_site/my-tracking.html'
    template_context = {}

    fb_app_id = getattr(settings, 'FACEBOOK_APP_ID', '')

    try:
        tracking = Tracking.objects.get(tracking_no=tracking_no.upper())
        tracking_events = TrackingEvent.objects.filter(tracking=tracking.id).order_by('-datetime')

        template_context.update({
            'tracking': tracking,
            'tracking_events': tracking_events,
        })
    except Tracking.DoesNotExist:
        # Ticket Order
        template_context.update({
            'tracking': False
        })

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_tracking(request):
    template_name = 'public_site/tracking.html'

    last_events = Tracking.objects.all().values('last_event')
    data = {}
    keynames = {
        1: 'tracking_erstellt',
        2: 'eingang_velafrica_partner',
        4: 'containerverlad',
        5: 'ankunft_afrika',
        6: 'verkauf',
        7: 'zerlegung',
        8: 'export'
    }
    for id in last_events:
        last_event_event_type = TrackingEvent.objects.get(id=id.get('last_event')).event_type
        keyname = keynames.get(last_event_event_type.id, last_event_event_type.name)
        if keyname in data:
            data[keyname] += 1
        else:
            data[keyname] = 1

    data['weg_afrika'] = data.get('export', 0) + data.get('containerverlad', 0)

    tracking_created_id = 1

    data['tracking_erstellt'] = TrackingEvent.objects.filter(event_type_id=tracking_created_id).count()
    data['total'] = Tracking.get_tracked_velo_count(this_year=True, without_initial=True)

    template_context = {
        'data': data
    }

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))


def render_partners(request):
    template_name = 'public_site/partner.html'

    if 'afrika' in request.path:
        choice = 1
        section_id = 'africa'
    elif 'schweiz' in request.path:
        choice = 2
        section_id = 'swiss'

    partners_locations = Partner.objects.filter(country=choice).order_by('location').values('location').distinct()
    dict = {}
    for location in partners_locations:
        keyname = location['location']
        dict[keyname] = Partner.objects.filter(country=choice).filter(location=location['location'])

    dict = collections.OrderedDict(sorted(dict.items()))

    template_context = {
        'section_id': section_id,
        'locations': dict
    }

    return render_to_response(template_name, template_context, context_instance=RequestContext(request))
