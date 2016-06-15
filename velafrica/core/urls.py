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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from velafrica.core import views
from velafrica.counter import views as counter_views
from velafrica.organisation.views import MunicipalityAutocomplete
from velafrica.stock.views import ProductAutocomplete, WarehouseAutocomplete

urlpatterns = [
	#url(r'^$', views.home, name='home'),
    url(r'^api/', include('velafrica.api.urls')),

    url(r'^$', RedirectView.as_view(url='/tracking')),
	url(r'^counter', counter_views.counter, name='counter'),
    url(r'^download', views.downloads, name='download'),
    url(r'^stock', views.stock, name='stock'),
    url(r'^tracking/(?P<tracking_no>\w+)', views.tracking, name='tracking_detail'),
    url(r'^tracking', views.tracking, name='tracking'),
    url(r'^transport', views.transport, name='transport'),
    url(r'^container', views.container, name='container'),

    url(r'^auth/login', auth_views.login, {'template_name':'auth/login.html'}, name='login'),
    url(r'^auth/password/reset', 
        auth_views.password_reset, 
        {'post_reset_redirect' : '/auth/password/reset/done/'}, 
        name='password_reset'
    ),
    url(r'^auth/password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^auth/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        auth_views.password_reset_confirm, 
        {'post_reset_redirect' : '/auth/password/done/'}, name='password_reset_confirm'
    ),
    url(r'^auth/password/done/$', 
        auth_views.password_reset_complete, name='password_reset_complete'
    ),

    url(r'^auth/profile', views.profile, name='profile'),
    url(r'^auth/logout', views.accounts_logout, name='logout'),

    # autocomplete urls
    url(r'^municipality-autocomplete/$', MunicipalityAutocomplete.as_view(), name='municipality-autocomplete'),
    url(r'^product-autocomplete/$', ProductAutocomplete.as_view(), name='product-autocomplete'),
    url(r'^warehouse-autocomplete/$', WarehouseAutocomplete.as_view(), name='warehouse-autocomplete'),

    # admin urls
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include("massadmin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
