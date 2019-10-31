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
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import *

from velafrica.core import views
from velafrica.public_site import views as velafrica_public_site_views
from velafrica.stock import views as stock_views
from velafrica.transport import views as transport_views
from velafrica.core.autocomplete import urls as autocomplete_urls

app_name = "core"

# frontend = [
#     url(r'^$', RedirectView.as_view(url='/velo_tracking')),
#     url(r'^counter', counter_views.counter, name='counter'),
#     url(r'^download', download_views.downloads, name='download'),
#     url(r'^stock', stock_views.stock, name='stock'),
#     url(r'^velo_tracking/(?P<tracking_no>\w+)', sbbtracking_views.tracking, name='tracking_detail'),
#     url(r'^velo_tracking', sbbtracking_views.tracking, name='tracking'),
#     url(r'^transport', transport_views.transport, name='transport'),
#     url(r'^warehouses', stock_views.warehouses, name='warehouses'),
#     url(r'^warehouse/(?P<pk>[0-9]+)', stock_views.warehouse, name='warehouse_detail'),
#     url(r'^container', velafrica_sud_views.container, name='container'),
#     url(r'^bikes', ListView.as_view(model=Bike), name='bike'),
#     url(r'^collection', collection_views.collection, name='collection'),
# ]

auth = [
    url(r'^login', LoginView.as_view(template_name='auth/login.html'), name='login'),
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
                  url(r'^', include('velafrica.frontend.urls')),

                  # urls for the public pages (django cms)
                  url(r'^cms/', include('velafrica.public_site.urls')),
                  url(r'^socialwall$', velafrica_public_site_views.render_template, name='socialwall'),
                  url(r'^collection-point$', velafrica_public_site_views.render_template, name='home'),
                  url(r'^collection-event$', velafrica_public_site_views.render_template, name='home'),

                  # api urls
                  url(r'^api/', include('velafrica.api.urls')),
                  # api auth
                  url(r'^api-auth/', include('rest_framework.urls')),

                  # auth related urls
                  url(r'^auth/', include((auth, app_name), namespace='auth')),
                  # url to request Password reset
                  url(r'^auth/password/reset/$',
                      PasswordResetView.as_view(),
                      {'post_reset_redirect': '/auth/password/reset/done/'},
                      name='password_reset'
                      ),
                  # url to show after password reset request
                  url(r'^auth/password/reset/done/$',
                      PasswordResetDoneView.as_view(),
                      name='password_reset_done'
                      ),
                  # url that gets sent via email to the user
                  url(r'^auth/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                      PasswordResetConfirmView.as_view(),
                      {'post_reset_redirect': '/auth/password/reset/complete/'}, name='password_reset_confirm'
                      ),
                  # final site of password reset
                  url(r'^auth/password/reset/complete/$',
                      PasswordResetCompleteView.as_view(),
                      name='password_reset_complete'
                      ),

                  url(r'^autocomplete/', include(autocomplete_urls)),

                  # admin doc urls
                  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                  # admin urls
                  url(r'^admin/', admin.site.urls),
                  url(r'^admin/', include("massadmin.urls")),
                  url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                  url(r'^paypal/', include('paypal.standard.ipn.urls')),
                  # url(r'^admin/mailchimp', include(mailchimp_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# make cms available
urlpatterns += i18n_patterns()
