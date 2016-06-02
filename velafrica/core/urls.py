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
from django.contrib.auth import views
from django.contrib.auth.views import password_reset
from django.views.generic import RedirectView
from velafrica.core import views

urlpatterns = [
	#url(r'^$', views.home, name='home'),
    url(r'^$', RedirectView.as_view(url='/tracking')),
	url(r'^counter', views.counter, name='counter'),
    url(r'^download', views.downloads, name='download'),
    url(r'^stock', views.stock, name='stock'),
    url(r'^tracking/(?P<tracking_no>\w+)', views.tracking, name='tracking_detail'),
    url(r'^tracking', views.tracking, name='tracking'),
    url(r'^transport', views.transport, name='transport'),
    url(r'^container', views.container, name='container'),

    url(r'^auth/login', 'django.contrib.auth.views.login', {'template_name':'auth/login.html'}, name='login'),
    url(r'^auth/password/reset', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/auth/password/reset/done/'}, 
        name='password_reset'
    ),
    url(r'^auth/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^auth/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/auth/password/done/'}, name='password_reset_confirm'
    ),
    url(r'^auth/password/done/$', 
        'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'
    ),

    url(r'^auth/profile', views.profile, name='profile'),
    url(r'^auth/logout', views.accounts_logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include("massadmin.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
