from dal import autocomplete
from django.db.models import Q
from django.shortcuts import render
from velafrica.organisation.models import Municipality


class MunicipalityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Municipality.objects.none()

        qs = Municipality.objects.all()

        if self.q:
            qs = qs.filter(Q(plz_name__icontains=self.q) | Q(name__icontains=self.q) | Q(name_short__icontains=self.q) | Q(plz__startswith=self.q))

        return qs