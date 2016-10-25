from django.conf.urls import include, url
from .views import order_invoice

urlpatterns = [
    url(r'^orderinvoice/$', order_invoice, name="orderinvoice")
]
