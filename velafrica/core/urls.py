# -*- coding: utf-8 -*-
"""velafrica_trackingtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from velafrica.collection import views as collection_views
from velafrica.core import views
from velafrica.counter import views as counter_views
from velafrica.download import views as download_views
from velafrica.public_site import views as velafrica_public_site_views
from velafrica.sbbtracking import views as sbbtracking_views
from velafrica.stock import views as stock_views
from velafrica.transport import views as transport_views
from velafrica.velafrica_sud import views as velafrica_sud_views

frontend = [
    url(r'^$', RedirectView.as_view(url='/velo_tracking')),
    url(r'^counter', counter_views.counter, name='counter'),
    url(r'^download', download_views.downloads, name='download'),
    url(r'^stock', stock_views.stock, name='stock'),
    url(r'^velo_tracking/(?P<tracking_no>\w+)', sbbtracking_views.tracking, name='tracking_detail'),
    url(r'^velo_tracking', sbbtracking_views.tracking, name='tracking'),
    url(r'^transport', transport_views.transport, name='transport'),
    url(r'^warehouses', stock_views.warehouses, name='warehouses'),
    url(r'^warehouse/(?P<pk>[0-9]+)', stock_views.warehouse, name='warehouse_detail'),
    url(r'^container', velafrica_sud_views.container, name='container'),
    url(r'^collection', collection_views.collection, name='collection'),

]

auth = [
    url(r'^login', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^logout', views.accounts_logout, name='logout'),
]

autocomplete = [
    # autocomplete urls
    url(r'^product/$', stock_views.ProductAutocomplete.as_view(), name='product'),
    url(r'^warehouse/$', stock_views.WarehouseAutocomplete.as_view(), name='warehouse'),
    url(r'^driver/$', transport_views.DriverAutocomplete.as_view(), name='driver'),
]

# main configuration
urlpatterns = [

                  url(r'^', include(frontend, namespace="frontend")),

                  # urls for the public pages (django cms)
                  url(r'^cms/', include('velafrica.public_site.urls', namespace='home')),
                  url(r'^socialwall$', velafrica_public_site_views.render_template, name='socialwall'),
                  url(r'^collection-point$', velafrica_public_site_views.render_template, name='home'),
                  url(r'^collection-event$', velafrica_public_site_views.render_template, name='home'),

                  # api urls
                  url(r'^api/', include('velafrica.api.urls', namespace="api")),
                  # api auth
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  # auth related urls
                  url(r'^auth/', include(auth, namespace="auth")),
                  # url to request Password reset
                  url(r'^auth/password/reset/$',
                      auth_views.password_reset,
                      {'post_reset_redirect': '/auth/password/reset/done/'},
                      name='password_reset'
                      ),
                  # url to show after password reset request
                  url(r'^auth/password/reset/done/$',
                      auth_views.password_reset_done,
                      name='password_reset_done'
                      ),
                  # url that gets sent via email to the user
                  url(r'^auth/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                      auth_views.password_reset_confirm,
                      {'post_reset_redirect': '/auth/password/reset/complete/'}, name='password_reset_confirm'
                      ),
                  # final site of password reset
                  url(r'^auth/password/reset/complete/$',
                      auth_views.password_reset_complete, name='password_reset_complete'
                      ),

                  url(r'^autocomplete/', include(autocomplete, namespace="autocomplete")),

                  # admin doc urls
                  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                  # admin urls
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^admin/', include("massadmin.urls")),
                  url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                  url(r'^paypal/', include('paypal.standard.ipn.urls')),
                  # url(r'^admin/mailchimp', include(mailchimp_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# make cms available
urlpatterns += i18n_patterns(url(r'^pages/', include('cms.urls'), name="cms"))
