# -*- coding: utf-8 -*-
from dal import autocomplete
from django.db.models import Q
from django.shortcuts import render
from velafrica.stock.models import Product, Warehouse


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(Q(name__contains=self.q) | Q(articlenr__contains=self.q))

        return qs

class WarehouseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        qs = Warehouse.objects.all()

        if self.q:
            qs = qs.filter(Q(name__contains=self.q) | Q(organisation__name__contains=self.q))

        return qs